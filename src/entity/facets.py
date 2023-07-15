from __future__ import annotations

from typing import List, Optional

from pandas import DataFrame
from pydantic import BaseModel


class TRANSACTTYPEItem(BaseModel):
    id: str
    label: str


class CLAS(BaseModel):
    id: str
    label: str


class PROJECTPHASEINFOItem(BaseModel):
    id: str


class RESCOMItem(BaseModel):
    id: str
    label: str


class PROPERTYTYPEItem(BaseModel):
    id: str
    label: str


class FURNISHItem(BaseModel):
    id: str
    label: str


class BUILDINGIDItem(BaseModel):
    id: str
    label: str


class LOCALITYIDItem(BaseModel):
    id: str
    label: str
    rating: Optional[float] = None


class FEATURE(BaseModel):
    id: str
    label: str


class FACINGDIRECTIONItem(BaseModel):
    id: str
    label: str


class CITYItem(BaseModel):
    id: str
    label: str


class AVAILABILITYItem(BaseModel):
    id: str
    label: str


class APPROVEDFORINDUSTRYItem(BaseModel):
    id: str
    label: str


class PREFERENCEItem(BaseModel):
    id: str
    label: str


class OWNERSHIPTYPEItem(BaseModel):
    id: str
    label: str


class FacetsEntity(BaseModel):
    TRANSACT_TYPE: List[TRANSACTTYPEItem]
    CLASS: List[CLAS]
    PROJECT_PHASE_INFO: List[PROJECTPHASEINFOItem]
    RES_COM: List[RESCOMItem]
    PROPERTY_TYPE: List[PROPERTYTYPEItem]
    FURNISH: List[FURNISHItem]
    BUILDING_ID: List[BUILDINGIDItem]
    LOCALITY_ID: List[LOCALITYIDItem]
    FEATURES: List[FEATURE]
    FACING_DIRECTION: List[FACINGDIRECTIONItem]
    CITY: List[CITYItem]
    AVAILABILITY: List[AVAILABILITYItem]
    APPROVED_FOR_INDUSTRY: List[APPROVEDFORINDUSTRYItem]
    PREFERENCE: List[PREFERENCEItem]
    OWNERSHIP_TYPE: List[OWNERSHIPTYPEItem]

    @property
    def get_attrs(self) -> list[str]:
        return list(self.__dict__.keys())

    def to_df(self, attr: str) -> DataFrame:
        attrs = self.__dict__
        if attr not in attrs:
            raise AttributeError(
                f'"{attr}" not present in FacetsEntity class.'
            )

        data = [i.dict() for i in getattr(self, attr)]
        return DataFrame(data)
