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
        DFPath.data_dir.mkdir(exist_ok=True)

    async def extend_df(self, df: DataFrame, path: Path) -> DataFrame:
        logger.warning(f'"{path}" CSV file exists.')
        old_df = await asyncio.to_thread(pd.read_csv, path)
        new_df = pd.concat([old_df, df], axis=0, ignore_index=True)
        return new_df

    async def export_df_to_csv(self, df: DataFrame, fp: Path) -> None:
        if df.shape[0] == 0:
            logger.warning(f'Not writing into "{fp}".')
            return None

        async with aiofiles.open(fp, 'w') as f:
            logger.info(f'Writing data into "{fp}".')
            csv_data = df.to_csv(index=False, header=True)
            await f.write(csv_data)

    async def drop_duplicates(self, path: Path) -> None:
        df = await asyncio.to_thread(pd.read_csv, path)
        logger.warning('Drop %s rows from "%s"', df.duplicated().sum(), path)
        df = df.drop_duplicates(ignore_index=True)
        await self.export_df_to_csv(df, path)

    async def export_dfs(
        self,
        drop_duplicates: bool = False,
    ) -> None:
        facets_dfs = await asyncio.gather(
            *[self.data.facets.to_df(attr) for attr in self.data.facets.get_attrs]
        )
        projects_df = await self.data.to_df('projects')
        srp_df = await self.data.to_df('srp')

        for df, path in zip((projects_df, srp_df), (DFPath.projects, DFPath.srp)):
            if not path.exists():
                logger.warning(f'"{path}" CSV file not exists.')
                drop_duplicates = False
            else:
                df = await self.extend_df(df, path)

            logger.info(f'Shape{df.shape} - "{path}"')
            await self.export_df_to_csv(df, path)

            if drop_duplicates:
                await self.drop_duplicates(path)

        facets_dir = DFPath.facets_dir
        if not facets_dir.exists():
            facets_dir.mkdir()

        tasks = []
        for name, facet_df in zip(self.data.facets.get_attrs, facets_dfs):
            fp = facets_dir / f'{name}.csv'
            if fp.exists():
                continue
            logger.info(f'Shape{facet_df.shape} - {fp}')
            tasks.append(self.export_df_to_csv(facet_df, fp))

        await asyncio.gather(*tasks)
