from pathlib import Path

import pandas as pd

from src import utils
from src.logger import get_logger

AMENITIES_PATH = Path("data/facets/AMENITIES.csv")

logger = get_logger(__name__)


def amenities_to_csv() -> None:
    url = "https://www.99acres.com/api-aggregator/static-attributes?includedFields="
    amenities = utils.get_request(url)["propertyAmenity"]

    df = pd.DataFrame([j for i in amenities for j in amenities[i]["default"]])
    df = df.sort_values(by=["category", "id"])

    duplicated_idx = df[df["id"].duplicated()].index
    df = df.drop(columns=["url"], index=duplicated_idx)

    df.to_csv(AMENITIES_PATH, index=False)
    logger.info(f'Export: "{AMENITIES_PATH}"')


def main():
    amenities_to_csv()


if __name__ == "__main__":
    main()
