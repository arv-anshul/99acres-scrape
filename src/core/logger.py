import logging
from datetime import datetime as dt
from pathlib import Path


def get_logger(logger_name: str) -> logging.Logger:
    """
    :logger_name (str): `__name__`

    :returns: logging.Logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    fp = Path(f'logs/{dt.now():%d%m%y_%H%M}.log')
    fp.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s]:%(levelname)s - [%(lineno)d]:%(name)s - %(message)s"
    )

    file_handler = logging.FileHandler(fp)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
