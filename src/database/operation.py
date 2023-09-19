import asyncio
from pathlib import Path
from typing import NamedTuple

import aiofiles
import pandas as pd
from pandas import DataFrame

from src.core.logger import get_logger
from src.entity.acres99 import Acres99

logger = get_logger(__name__)


class DFPath(NamedTuple):
    data_dir = Path('data')
    projects = Path('data/projects.csv')
    srp = Path('data/srp.csv')
    facets_dir = Path('data/facets')


class DataFrameOperations:
    def __init__(self, data: Acres99):
        self.data = data

    async def __extend_df(self, df: DataFrame, path: Path) -> DataFrame:
        logger.warning(f'Extending: "{path}".')
        old_df = await asyncio.to_thread(pd.read_csv, path)
        new_df = pd.concat([old_df, df], axis=0, ignore_index=True)
        return new_df

    @staticmethod
    async def export_df_to_csv(df: DataFrame, fp: Path) -> None:
        if df.shape[0] == 0:
            logger.warning(f'Not writing into "{fp}".')
            return None

        async with aiofiles.open(fp, 'w') as f:
            logger.info(f'Exporting: Shape{df.shape} at {fp}.')
            csv_data = df.to_csv(index=False, header=True)
            await f.write(csv_data)

    async def _drop_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.warning('Drop %s rows.', df.duplicated(['PROP_ID']).sum())
        df = df.drop_duplicates(['PROP_ID'], keep='last')
        return df

    async def export_df(self, df: DataFrame, path: Path) -> None:
        if not path.exists():
            logger.warning(f'"{path}" CSV file not exists.')
        else:
            df = await self.__extend_df(df, path)

        df = await self._drop_duplicates(df)
        await self.export_df_to_csv(df, path)

    async def export_facets_df(self, dir_path: Path):
        dir_path.mkdir(exist_ok=True)

        facets_dfs: list[DataFrame] = await asyncio.gather(
            *[self.data.facets.to_df(attr) for attr in self.data.facets.get_attrs]
        )

        tasks = []
        for name, facet_df in zip(self.data.facets.get_attrs, facets_dfs):
            fp = dir_path / f'{name}.csv'
            if fp.exists():
                continue
            await self.export_df_to_csv(facet_df, fp)

        return await asyncio.gather(*tasks)
