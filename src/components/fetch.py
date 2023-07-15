"""
Fetch all the required data from 99acres.com website using its APIs.
"""

import json
from pathlib import Path
from typing import Any

from requests import RequestException, Response, get

from src.core.logger import get_logger

logger = get_logger(__name__)
REQUESTS_PATH = Path('requests.json')


def get_requests_json() -> dict[str, Any]:
    if not REQUESTS_PATH.exists():
        raise FileNotFoundError(
            f'No requests JSON file exists. Make one at "{REQUESTS_PATH}".'
        )
    return json.load(open(REQUESTS_PATH))


def update_url_params(
    params_dict: dict, page_num: int, page_size: int,
) -> dict:
    if page_size > 1500:
        raise ValueError('page_size <= 1500')
    params_dict['page_num'] = str(page_num)
    params_dict['page_size'] = str(page_size)
    return params_dict


def response(
    page_num: int, page_size: int = 500, **kwargs,
) -> Response:
    """
    :page_num (int): Page number.
    :page_size (int): No. of properties data. Default as 500 properties data.

    :returns: requests.Response
    """
    if len(kwargs) == 0:
        kwargs = get_requests_json()

    kwargs['params'] = update_url_params(
        kwargs['params'], page_num, page_size,
    )

    r = get(**kwargs)
    msg = 'Status[%s]: %s' % (r.status_code, kwargs['url'])

    if r.status_code > 200:
        logger.exception(msg)
        raise RequestException(msg)
    logger.info(msg)
    return r
