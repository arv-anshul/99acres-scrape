from typing import Any, Generator

import httpx

from src.constants import REQUEST_HEADERS
from src.logger import get_logger

logger = get_logger(__name__)


def get_request(url: str) -> dict[str, Any]:
    r = httpx.get(url=url, headers=REQUEST_HEADERS)
    logger.info(f"[{r.status_code}]:{r.url}")
    r.raise_for_status()
    return r.json()


def progress_bar_nums(n_pages: int) -> Generator[float, None, None]:
    for i in range(1, n_pages + 1):
        yield i * (1 / n_pages)
