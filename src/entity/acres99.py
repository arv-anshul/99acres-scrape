from pandas import DataFrame
from pydantic import BaseModel

from src.core.logger import get_logger

from .facets import FacetsEntity
from .project import ProjectEntity
from .srp import SRPEntity

logger = get_logger(__name__)


class Acres99(BaseModel):
    facets: FacetsEntity
    projects: list[ProjectEntity]
    srp: list[SRPEntity]

    async def to_df(self, attr: str) -> DataFrame:
        if attr not in self.__dict__.keys():
            raise AttributeError(f'"{attr}" not in {self.__class__.__name__}')

        if attr == 'facets':
            raise NotImplementedError('Get `facets` DataFrame with `.facets` attribute.')

        df = DataFrame([i.model_dump() for i in getattr(self, attr)])
        return df
