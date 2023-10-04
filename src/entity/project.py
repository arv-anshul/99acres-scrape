from typing import List, Optional

from pydantic import BaseModel


class PossessionStatus(BaseModel):
    label: str


class LandingPage(BaseModel):
    url: str


class KeyHighlights(BaseModel):
    heading: str
    tuples: List[str]


class Tag(BaseModel):
    id: str


class LandMark(BaseModel):
    subHeading: str
    category: str


class LocationHighlights(BaseModel):
    heading: str
    landMarks: List[LandMark]


class Price(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None
    authentic: bool
    label: str


class Location(BaseModel):
    localityName: str
    projectName: str
    cityName: str
    stateName: str
    latitude: float
    stateId: str
    cityId: str
    localityId: str
    longitude: float


class Area(BaseModel):
    min: int
    max: int


class Price1(BaseModel):
    min: int
    max: int


class ConfigInfo(BaseModel):
    subLabel: str
    label: Optional[str] = None


class Card(BaseModel):
    area: Optional[Area] = None
    price: Price1
    configInfo: ConfigInfo


class ConfigSummary(BaseModel):
    cards: List[Card]


class Description(BaseModel):
    text: str


class ProjectEntity(BaseModel):
    rescom: str
    preference: str
    projectUnitId: str
    possessionStatus: PossessionStatus
    heading: str
    landingPage: LandingPage
    tags: List[Tag]
    locationHighlights: Optional[LocationHighlights] = None
    subHeading: str
    price: Price
    location: Location
    entityType: str
    configSummary: ConfigSummary
    description: Optional[Description] = None
