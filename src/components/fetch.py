import json
from pathlib import Path
from typing import Any, Literal

import aiohttp

from src.core.logger import get_logger

logger = get_logger(__name__)
REQUESTS_PATH = Path('requests.json')


def get_requests_json() -> dict[str, Any]:
    if not REQUESTS_PATH.exists():
        raise FileNotFoundError(
            f'No requests JSON file exists. Make one at "{REQUESTS_PATH}".'
        )
    return json.load(open(REQUESTS_PATH))


async def update_url_params(
    params_dict: dict, page_num: int, page_size: int,
) -> dict:
    if page_size > 1500:
        raise ValueError('page_size <= 1500')
    params_dict['page_num'] = str(page_num)
    params_dict['page_size'] = str(page_size)
    return params_dict


async def response(
    page_num: int,
    page_size: int = 500,
    return_type: Literal['json', 'text'] = 'json',
    **kwargs,
) -> dict[str, Any] | str:
    """
    :page_num (int): Page number.
    :page_size (int): No. of properties data. Default as 500 properties data.

    :returns: aiohttp.ClientResponse
    """
    if len(kwargs) == 0:
        kwargs = get_requests_json()

    kwargs['params'] = await update_url_params(
        kwargs['params'], page_num, page_size,
    )

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(**kwargs) as r:
                print(r.url)
                msg = 'Status[%s]: %s' % (r.status, r.url)
                if r.status > 200:
                    logger.exception(msg)
                    raise aiohttp.ClientResponseError(
                        request_info=r.request_info,
                        history=(r,),
                        status=r.status,
                        message=msg,
                    )
                logger.info(msg)

                if return_type == 'json':
                    return await r.json()
                else:
                    return await r.text()
        except aiohttp.ClientResponseError as cre:
            logger.exception(f'Error fetching response: {cre}')
            raise cre
