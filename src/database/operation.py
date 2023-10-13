from pathlib import Path
from typing import NamedTuple

import pandas as pd

from src.core.logger import get_logger

logger = get_logger(__name__)


class DFPath(NamedTuple):
    data_dir = Path('data')
    projects = Path('data/projects.csv')
    srp = Path('data/srp.csv')
    facets_dir = Path('data/facets')


async def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    logger.warning('Drop %s rows.', df.duplicated(['PROP_ID']).sum())
    df = df.drop_duplicates(['PROP_ID'], keep='last')
    return df
