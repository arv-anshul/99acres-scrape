from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class MAPDETAILS(BaseModel):
    LATITUDE: str
    LONGITUDE: str


class FORMATTEDLANDMARKDETAIL(BaseModel):
    text: str


class Location(BaseModel):
    CITY: str
    CITY_NAME: str
    BUILDING_ID: str
    BUILDING_NAME: str
    SOCIETY_NAME: str
    LOCALITY_ID: str
    LOCALITY_NAME: str
    ADDRESS: Optional[str] = None


class SRPEntity(BaseModel):
    SPID: str
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
    REGISTER_DATE: str
    POSTING_DATE: Optional[int] = None
    UPDATE_DATE: int
    CLASS: str
    RES_COM: str
    PROP_NAME: str
    PROPERTY_NUMBER: str
    MIN_PRICE: str
    MAX_PRICE: str
    PRICE_SQFT: str
    PROJ_ID: str
    BUILDING_ID: str
    VERIFIED: str
    MAP_DETAILS: MAPDETAILS
    MIN_AREA_SQFT: str
    MAX_AREA_SQFT: str
    AMENITIES: str
    ALT_TAG: Optional[str] = None
    PRODUCT_TYPE: str
    TOP_USPS: Optional[List[str]] = None
    EXPIRY_DATE: str
    PROPERTY_TYPE__U: str
    AREA: str
    SECONDARY_AREA: str
    PRICE: str
    PROP_HEADING: str
    VALUE_LABEL: str
    CLASS_HEADING: str
    CLASS_LABEL: str
    REGISTER_DATE__U: str
    REGISTERED_DAYS: str
    PRIMARY_TAGS: List
    SECONDARY_TAGS: List[str]
    TOTAL_LANDMARK_COUNT: Optional[int] = None
    FORMATTED_LANDMARK_DETAILS: Optional[List[FORMATTEDLANDMARKDETAIL]] = None
    SOCIETY_NAME: str
    BUILDING_NAME: str
    location: Location
    BALCONY_NUM: Optional[str] = None
    FLOOR_NUM: Optional[str] = None

    @property
    def get_attrs(self) -> list[str]:
        return list(self.__dict__.keys())
