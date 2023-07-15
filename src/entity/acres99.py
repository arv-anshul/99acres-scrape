from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import List

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

    def to_df(self, attr: str):
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

    def _extend_df(
        self, df: DataFrame, path: DFPath,
    ) -> DataFrame:
        if not path.value.exists():
            return df

        old_df = pd.read_csv(path.value)
        new_df = pd.concat([old_df, df], axis=0, ignore_index=True)
        return new_df

    def _export_facets_df(self, facets_dfs: list[dict[str, DataFrame]]):
        facets_dir = DFPath.FACETS_DIR.value
        if not facets_dir.exists():
            facets_dir.mkdir()

        for facet in facets_dfs:
            for name, df in facet.items():
                fp = facets_dir / f'{name}.csv'
                if fp.exists():
                    continue
                logger.info(f'Shape{df.shape} - {fp}')
                df.to_csv(fp, index=False)

    def _drop_duplicates(self, path: DFPath) -> None:
        df = pd.read_csv(path.value)
        logger.warning(
            'Drop %s rows from "%s"', df.duplicated().sum(), path.value
        )
        df = df.drop_duplicates(ignore_index=True)
        df.to_csv(path.value)

    def export_dfs(
        self, extend: bool = True, drop_duplicates: bool = False,
    ) -> None:
        """
        Export all the data as DataFrames at pre-defined paths.
        """
        # Get the current DataFrames
        facets_dfs = [
            {i: self.facets.to_df(i)} for i in self.facets.get_attrs
        ]
        projects_df = self.to_df('projects')
        srp_df = self.to_df('srp')

        for df, path in zip(
            (projects_df, srp_df), (DFPath.PROJECTS, DFPath.SRP)
        ):
            # Extend the DataFrames
            if extend:
                df = self._extend_df(df, path)
            else:
                if path.value.exists():
                    raise FileExistsError(
                        f'"{path.value}" already exists.'
                    )

            # Export the projects and srp DataFrames after extending them
            logger.info(f'Shape{df.shape} - "{path.value}"')
            df.to_csv(path.value, index=False)

            # Drop duplicates from the DataFrames
            if drop_duplicates:
                self._drop_duplicates(path)

        # Export facets DataFrames if not exists
        self._export_facets_df(facets_dfs)
