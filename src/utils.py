from typing import Any

import httpx

from src.logger import get_logger

logger = get_logger(__name__)

REQUEST_HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

SRP_DATA_COLUMNS = [
    "AGE",
    "AMENITIES",
    "AREA",
    "BALCONY_NUM",
    "BATHROOM_NUM",
    "BEDROOM_NUM",
    "BROKERAGE",
    "BUILDING_ID",
    "BUILDING_NAME",
    "BUILTUP_SQFT",
    "CARPET_SQFT",
    "CITY_ID",
    "CITY",
    "CLASS_HEADING",
    "CLASS_LABEL",
    "COMMON_FURNISHING_ATTRIBUTES",
    "CONTACT_COMPANY_NAME",
    "CONTACT_NAME",
    "DEALER_PHOTO_URL",
    "DESCRIPTION",
    "EXPIRY_DATE",
    "FACING",
    "FEATURES",
    "FLOOR_NUM",
    "FORMATTED_LANDMARK_DETAILS",
    "FORMATTED",
    "FSL_Data",
    "FURNISH",
    "FURNISHING_ATTRIBUTES",
    "GROUP_NAME",
    "LISTING",
    "LOCALITY_WO_CITY",
    "LOCALITY",
    "location",
    "MAP_DETAILS",
    "MAX_AREA_SQFT",
    "MAX_PRICE",
    "MEDIUM_PHOTO_URL",
    "metadata",
    "MIN_AREA_SQFT",
    "MIN_PRICE",
    "OWNTYPE",
    "PD_URL",
    "PHOTO_URL",
    "PREFERENCE",
    "PRICE_PER_UNIT_AREA",
    "PRICE_SQFT",
    "PRICE",
    "profile",
    "PROP_DETAILS_URL",
    "PROP_HEADING",
    "PROP_ID",
    "PROP_NAME",
    "PROPERTY_IMAGES",
    "PROPERTY_TYPE",
    "QUALITY_SCORE",
    "REGISTER_DATE",
    "SECONDARY_TAGS",
    "SOCIETY_NAME",
    "SUPER_SQFT",
    "SUPERBUILTUP_SQFT",
    "THUMBNAIL_IMAGES",
    "TOP_USPS",
    "TOTAL_FLOOR",
    "TOTAL_LANDMARK_COUNT",
    "TRANSACT_TYPE",
    "xid",
]


def get_request(url: str) -> dict[str, Any]:
    r = httpx.get(url=url, headers=REQUEST_HEADERS)
    logger.info(f"[{r.status_code}]:{r.url}")
    r.raise_for_status()
    return r.json()


def progress_bar_nums(page_nums: list[int] | range):
    n = len(page_nums)
    for i in range(1, n + 1):
        yield i * (1 / n)
