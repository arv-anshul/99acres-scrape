import json
from pathlib import Path

from src import utils

CITY_W_ID_PATH = Path("data/city_w_id.json")


def get_city_w_id_dict() -> dict[int, str]:
    url = "https://www.99acres.com/api-aggregator/content/locations/group/PROPERTY_CITY?rtype=json"
    data: list[dict[str, str]] = utils.get_request(url)["locationDropDowns"]
    ids = [int(i["locationId"].split("_")[0]) for i in data]
    cities = [i["label"] for i in data]
    return dict(zip(ids, cities))


def save_city_w_id_dict() -> None:
    CITY_W_ID_PATH.parent.mkdir(exist_ok=True)
    with open(CITY_W_ID_PATH, "w") as f:
        json.dump(get_city_w_id_dict(), f, indent=2, sort_keys=True)


if __name__ == "__main__":
    save_city_w_id_dict()
