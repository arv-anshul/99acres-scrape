import json
from pathlib import Path

from src import utils

CITY_W_ID_PATH = Path("data/city_w_id.json")


def store_city_w_id_mapping() -> None:
    url = "https://www.99acres.com/api-aggregator/content/locations/group/PROPERTY_CITY?rtype=json"
    data: list[dict[str, str]] = utils.get_request(url)["locationDropDowns"]
    ids = [int(i["locationId"].split("_")[0]) for i in data]
    cities = [i["label"] for i in data]

    CITY_W_ID_PATH.parent.mkdir(exist_ok=True)
    with open(CITY_W_ID_PATH, "w") as f:
        json.dump(dict(zip(ids, cities)), f, indent=2, sort_keys=True)


if __name__ == "__main__":
    store_city_w_id_mapping()
