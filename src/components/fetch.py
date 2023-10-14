import json
from pathlib import Path
from typing import Any

import httpx
from streamlit.elements.lib.mutable_status_container import StatusContainer

from src.logger import get_logger
from src.utils import progress_bar_nums

logger = get_logger(__name__)

BASE_REQUESTS_PATH = Path('base.requests.json')
REQUESTS_PATH = Path('requests.json')


def get_requests_json() -> dict[str, Any]:
    if REQUESTS_PATH.exists():
        with REQUESTS_PATH.open() as f:
            return json.load(f)

    with BASE_REQUESTS_PATH.open() as f:
        return json.load(f)


def __update_url_params(params_dict: dict, page_num: int, prop_per_page: int) -> dict:
    if prop_per_page > 800:
        raise ValueError(f'page_size <= {prop_per_page}')
    params_dict['page'] = str(page_num)
    params_dict['page_size'] = str(prop_per_page)
    return params_dict


async def __fetch_response(session: httpx.AsyncClient, **get_requests_kwargs) -> dict:
    r = await session.get(**get_requests_kwargs, timeout=3)
    msg = f'[{r.status_code}]:{r.url}'
    logger.info(msg)

    if r.status_code > 200:
        logger.exception(msg)
        r.raise_for_status()

    return r.json()


async def fetch_all_responses(
    page_nums: list[int],
    prop_per_page: int,
    city_id: int,
    *,
    status: StatusContainer,
    **get_requests_kwargs,
) -> list[dict]:
    if len(get_requests_kwargs) == 0:
        get_requests_kwargs = get_requests_json()
    get_requests_kwargs['params']['city'] = city_id

    _ = progress_bar_nums(page_nums)
    progress = status.progress(
        0,
        f'🪝 Fetching Data of Page {page_nums[0]}/{page_nums[-1]}. '
        f'(Total {len(page_nums)} Pages)',
    )
    async with httpx.AsyncClient() as session:
        responses = []
        for i, page_num in zip(_, page_nums):
            get_requests_kwargs['params'] = __update_url_params(
                get_requests_kwargs['params'], page_num, prop_per_page
            )

            try:
                progress.progress(
                    i,
                    f'🪝 Fetching Data of Page {page_num}/{page_nums[-1]}. '
                    f'(Total {len(page_nums)} Pages)',
                )
                responses.append(await __fetch_response(session, **get_requests_kwargs))
            except Exception as e:
                logger.exception(e)
                print(f'**ERROR**: {e}')
                return responses

    return responses
