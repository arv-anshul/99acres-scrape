import json

import pandas as pd

from src.utils import request


def city_with_id_data() -> dict[int, str]:
    url = "https://www.99acres.com/api-aggregator/content/locations/group/PROPERTY_CITY?rtype=json"
    data: list[dict[str, str]] = json.loads(request(url))["locationDropDowns"]
    ids = [int(i["locationId"].split("_")[0]) for i in data]
    cities = [i["label"] for i in data]
    return dict(zip(ids, cities, strict=False))


def amenities_data() -> pd.DataFrame:
    url = "https://www.99acres.com/api-aggregator/static-attributes?includedFields="
    amenities = json.loads(request(url))["propertyAmenity"]

    df = pd.DataFrame([j for i in amenities for j in amenities[i]["default"]])
    df = df.sort_values(by=["category", "id"])

    duplicated_idx = df[df["id"].duplicated()].index
    return df.drop(columns=["url"], index=duplicated_idx)
