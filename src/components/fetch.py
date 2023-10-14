import asyncio
import json
from pathlib import Path
from typing import Any

import httpx

from src.logger import get_logger

logger = get_logger(__name__)

BASE_REQUESTS_PATH = Path('base.requests.json')
REQUESTS_PATH = Path('requests.json')


def get_requests_json() -> dict[str, Any]:
    if REQUESTS_PATH.exists():
        with REQUESTS_PATH.open() as f:
            return json.load(f)

    with BASE_REQUESTS_PATH.open() as f:
        return json.load(f)


def update_url_params(
    params_dict: dict,
    page_num: int,
    prop_per_page: int,
) -> dict[str, str]:
    if prop_per_page > 800:
        raise ValueError(f'page_size <= {prop_per_page}')
    params_dict['page'] = str(page_num)
    params_dict['page_size'] = str(prop_per_page)
    return params_dict


async def fetch_response(
    session: httpx.AsyncClient,
    **kwargs,
) -> dict:
    r = await session.get(**kwargs, timeout=3)
    msg = f'[{r.status_code}]:{r.url}'
    logger.info(msg)

    if r.status_code > 200:
        logger.exception(msg)
        r.raise_for_status()

    return r.json()


async def fetch_all_responses(
    page_nums: list[int],
    prop_per_page: int,
    city_id: int | None = None,
    **kwargs,
) -> list[dict]:
    """
    :page_num (int): Page number.
    :page_size (int): No. of properties data.

    :returns: List of aiohttp.ClientResponse
    """
    if len(kwargs) == 0:
        kwargs = get_requests_json()
    if city_id:
        kwargs['params']['city'] = city_id

    async with httpx.AsyncClient() as session:
        responses = []
        for page_num in page_nums:
            kwargs['params'] = update_url_params(kwargs['params'], page_num, prop_per_page)

            try:
                responses.append(await fetch_response(session, **kwargs))
            except Exception as e:
                logger.exception(e)
                print(f'**ERROR**: {e}')
                return responses

            await asyncio.sleep(0.03)

    return responses
