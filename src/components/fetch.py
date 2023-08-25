import json
from pathlib import Path
from typing import Any

import aiohttp

from src.core.logger import get_logger
from src.typing import Acres99Dict

from . import convert

logger = get_logger(__name__)

REQUESTS_PATH = Path('requests.json')


def get_requests_json() -> dict[str, Any]:
    if not REQUESTS_PATH.exists():
        raise FileNotFoundError(f'No requests JSON file exists. Make one at "{REQUESTS_PATH}".')
    return json.load(open(REQUESTS_PATH))


def update_url_params(
    params_dict: dict,
    page_num: int,
    prop_per_page: int,
) -> dict[str, str]:
    if prop_per_page > 1200:
        raise ValueError('page_size <= 1200')
    params_dict['page'] = str(page_num)
    params_dict['page_size'] = str(prop_per_page)
    return params_dict


async def fetch_response(
    session: aiohttp.ClientSession,
    **kwargs,
) -> Acres99Dict:
    try:
        async with session.get(**kwargs) as r:
            msg = 'Status[%s]: %s' % (r.status, r.url)
            logger.info(msg)

            if r.status > 200:
                logger.exception(msg)
                raise aiohttp.ClientResponseError(
                    request_info=r.request_info, history=(r,), status=r.status, message=msg
                )
            response = await r.json()

        return Acres99Dict(**await convert.convert_to_acres99_dict(response))

    except aiohttp.ClientResponseError as cre:
        logger.exception(f'Error fetching response: {cre}')
        raise cre


async def fetch_all_responses(
    page_nums: list[int],
    prop_per_page: int,
    city_id: int | None = None,
    **kwargs,
) -> list[Acres99Dict]:
    """
    :page_num (int): Page number.
    :page_size (int): No. of properties data.

    :returns: List of aiohttp.ClientResponse
    """
    if len(kwargs) == 0:
        kwargs = get_requests_json()

    if city_id:
        kwargs['params']['city'] = city_id

    async with aiohttp.ClientSession() as session:
        responses = []

        for p_num in page_nums:
            kwargs['params'] = update_url_params(kwargs['params'], p_num, prop_per_page)
            responses.append(await fetch_response(session, **kwargs))

    return responses
