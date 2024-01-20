from __future__ import annotations

import json
from typing import TYPE_CHECKING

import httpx

from src.constants import REQUESTS_JSON_PATH
from src.errors import ResquestsJsonNotFoundError
from src.logger import get_logger
from src.utils import progress_bar_nums

if TYPE_CHECKING:
    from streamlit.elements.lib.mutable_status_container import StatusContainer

logger = get_logger(__name__)


def __update_url_params(params_dict: dict, page_num: int, prop_per_page: int) -> dict:
    if prop_per_page > 800:
        raise ValueError(f"page_size <= {prop_per_page}")
    params_dict["page"] = str(page_num)
    params_dict["page_size"] = str(prop_per_page)
    return params_dict


async def __fetch_response(session: httpx.AsyncClient, **get_requests_kwargs) -> dict:
    try:
        r = await session.get(**get_requests_kwargs, timeout=3)
    except httpx.TimeoutException:
        logger.error(f"Timeout while requesting on {get_requests_kwargs['url']}")
        raise

    if r.status_code == 200:
        return r.json()
    logger.error(r.text)
    raise httpx.HTTPStatusError(
        f"{r.status_code}:{r.url}", request=r.request, response=r
    )


async def fetch_all_responses(
    page_nums: list[int],
    prop_per_page: int,
    city_id: int,
    *,
    status: StatusContainer,
    **get_requests_kwargs,
) -> list[dict]:
    if not get_requests_kwargs:
        if not REQUESTS_JSON_PATH.exists():
            raise ResquestsJsonNotFoundError(
                "Submit lateset curl command in app. Check documentation on: "
                "How to get the curl command?"
            )
        with REQUESTS_JSON_PATH.open() as f:
            get_requests_kwargs = json.load(f)

    get_requests_kwargs["params"]["city"] = city_id

    _ = progress_bar_nums(len(page_nums))
    progress = status.progress(
        0,
        f"🪝 Fetching Data of Page {page_nums[0]}/{page_nums[-1]}. "
        f"(Total {len(page_nums)} Pages)",
    )
    async with httpx.AsyncClient() as session:
        responses = []
        for i, page_num in zip(_, page_nums, strict=False):
            get_requests_kwargs["params"] = __update_url_params(
                get_requests_kwargs["params"], page_num, prop_per_page
            )

            try:
                progress.progress(
                    value=i,
                    text=f"🪝 Fetching Data of Page {page_num}/{page_nums[-1]}. "
                    f"(Total {len(page_nums)} Pages)",
                )
                responses.append(await __fetch_response(session, **get_requests_kwargs))
            except Exception as e:
                logger.exception(e)
                return responses

    return responses
