from __future__ import annotations

import asyncio
from enum import Enum
from pathlib import Path
from typing import List

import aiofiles
import pandas as pd
from pandas import DataFrame
from pydantic import BaseModel

from src.core.logger import get_logger

from .facets import FacetsEntity
from .project import ProjectEntity
from .srp import SRPEntity

logger = get_logger(__name__)


class DFPath(Enum):
    PROJECTS = Path('data/projects.csv')
    SRP = Path('data/srp.csv')
    FACETS_DIR = Path('data/facets')


class Acres99(BaseModel):
    facets: FacetsEntity
    projects: List[ProjectEntity]
    srp: List[SRPEntity]

    async def to_df(self, attr: str) -> pd.DataFrame:
        if attr not in self.__dict__.keys():
            raise AttributeError(
                f'"{attr}" not in {self.__class__.__name__}'
            )

        if attr == 'facets':
            raise NotImplementedError(
                f'Get `facets` DataFrame with `self.facets` attribute.'
            )

        df = DataFrame([i.dict() for i in getattr(self, attr)])
        return df

    async def _extend_df(
        self, df: DataFrame, path: DFPath,
    ) -> DataFrame:
        if not path.value.exists():
            return df

        old_df = await asyncio.to_thread(pd.read_csv, path.value)
        new_df = pd.concat([old_df, df], axis=0, ignore_index=True)
        return new_df

    async def _export_facets_df(
        self,
        facets_dfs: list[ DataFrame],
    ) -> None:
        facets_dir = DFPath.FACETS_DIR.value
        if not facets_dir.exists():
            facets_dir.mkdir()

        async def export_df_to_csv(df: DataFrame, fp: Path):
            async with aiofiles.open(fp, 'w') as f:
                csv_data = df.to_csv(index=False)
                await f.write(csv_data)

        tasks = []
        for name, facet_df in zip(self.facets.get_attrs, facets_dfs):
            fp = facets_dir / f'{name}.csv'
            if fp.exists():
                continue
            logger.info(f'Shape{facet_df.shape} - {fp}')
            tasks.append(export_df_to_csv(facet_df, fp))

        await asyncio.gather(*tasks)

    async def _drop_duplicates(self, path: DFPath) -> None:
        df = await asyncio.to_thread(pd.read_csv, path.value)
        logger.warning(
            'Drop %s rows from "%s"', df.duplicated().sum(), path.value
        )
        df = df.drop_duplicates(ignore_index=True)
        await asyncio.to_thread(df.to_csv, path.value, index=False)

    async def export_dfs(
        self, extend: bool = True, drop_duplicates: bool = False,
    ) -> None:
        """
        Export all the data as DataFrames at pre-defined paths.
        """
        # Get the current DataFrames
        facets_tasks = [self.facets.to_df(i) for i in self.facets.get_attrs]
        projects_task = self.to_df('projects')
        srp_task = self.to_df('srp')

        *facets_dfs, projects_df, srp_df = await asyncio.gather(
            *facets_tasks, projects_task, srp_task
        )

        for df, path in zip(
            (projects_df, srp_df), (DFPath.PROJECTS, DFPath.SRP)
        ):
            # Extend the DataFrames
            if extend:
                df = await self._extend_df(df, path)
            else:
                if path.value.exists():
                    raise FileExistsError(
                        f'"{path.value}" already exists.'
                    )

            # Export the projects and srp DataFrames after extending them
            logger.info(f'Shape{df.shape} - "{path.value}"')
            await asyncio.to_thread(df.to_csv, path.value, index=False)

            # Drop duplicates from the DataFrames
            if drop_duplicates:
                await self._drop_duplicates(path)

        # Export facets DataFrames if not exists
        await self._export_facets_df(facets_dfs)
