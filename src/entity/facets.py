from pandas import DataFrame
from pydantic import BaseModel


class BaseFacetsItem(BaseModel):
    id: str
    label: str


class FacetsEntity(BaseModel):
    PROPERTY_TYPE: list[BaseFacetsItem]
    FURNISH: list[BaseFacetsItem]
    LOCALITY_ID: list[BaseFacetsItem]
    FEATURES: list[BaseFacetsItem]
    FACING_DIRECTION: list[BaseFacetsItem]
    CITY: list[BaseFacetsItem]
    OWNERSHIP_TYPE: list[BaseFacetsItem]
    BEDROOM_NUM: list[BaseFacetsItem]
    BATHROOM_NUM: list[BaseFacetsItem]
    SUB_AVAILABILITY: list[BaseFacetsItem]

    @property
    def get_attrs(self) -> list[str]:
        return list(self.__dict__.keys())

    async def to_df(self, attr: str) -> DataFrame:
        attrs = self.__dict__
        if attr not in attrs:
            raise AttributeError(f'"{attr}" not present in FacetsEntity class.')

        data = [i.model_dump() for i in getattr(self, attr)]

        df = DataFrame(data).drop_duplicates()
        df['id'] = df['id'].str.zfill(3)
        df.sort_values(by='id', inplace=True)
        return df
