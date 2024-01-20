from typing import Generator

import httpx

from src.constants import REQUEST_HEADERS


def request(
    url: str,
    *,
    method: str = "GET",
    headers=REQUEST_HEADERS,
    timeout=5,
    **kwargs,
) -> bytes:
    r = httpx.request(
        method=method, url=url, headers=headers, timeout=timeout, **kwargs
    )
    r.raise_for_status()
    return r.content


def progress_bar_nums(n_pages: int) -> Generator[float, None, None]:
    for i in range(1, n_pages + 1):
        yield i * (1 / n_pages)
