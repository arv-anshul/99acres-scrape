from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class MAPDETAILS(BaseModel):
    LATITUDE: str
    LONGITUDE: str


class Location(BaseModel):
    CITY: str
    CITY_NAME: str
    LOCALITY_ID: str
    LOCALITY_NAME: str
    ADDRESS: Optional[str] = None


class SRPEntity(BaseModel):
    PROP_ID: str
    PREFERENCE: str
    DESCRIPTION: str
    PROPERTY_TYPE: str
    CITY: str
    TRANSACT_TYPE: str
    OWNTYPE: str
    BEDROOM_NUM: Optional[str]
    PRICE_PER_UNIT_AREA: str
    FURNISH: str
    FACING: int
    AGE: str
    TOTAL_FLOOR: Optional[str] = None
    FEATURES: str
    PROP_NAME: str
    PRICE_SQFT: str
    MAP_DETAILS: MAPDETAILS
    AMENITIES: Optional[str] = None
    AREA: str
    PRICE: str
    PROP_HEADING: str
    SECONDARY_TAGS: list[str]
    TOTAL_LANDMARK_COUNT: Optional[int] = None
    FORMATTED_LANDMARK_DETAILS: Optional[list[dict[str, str]]] = None
    SOCIETY_NAME: Optional[str] = None
    BUILDING_NAME: Optional[str] = None
    location: Location
    BALCONY_NUM: Optional[str] = None
    FLOOR_NUM: Optional[str] = None
    CARPET_SQFT: Optional[str] = None
    SUPERBUILTUP_SQFT: Optional[str] = None
    BUILTUP_SQFT: Optional[str] = None
    SUPER_SQFT: Optional[str] = None

    @property
    def get_attrs(self) -> list[str]:
        return list(self.__dict__.keys())
