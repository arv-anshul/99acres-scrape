from typing import Any

import pandas as pd
import requests

from src import utils
from src.logger import get_logger

amenities_fp = 'data/facets/AMENITIES.csv'

logger = get_logger(__name__)


def fetch_amenities_data() -> dict[str, Any]:
    r = requests.get(
        url='https://www.99acres.com/api-aggregator/static-attributes?includedFields=',
        headers=utils.request_headers,
    )
    logger.info(f"Status[{r.status_code}]:{r.url}")

    r.raise_for_status()
    return r.json()['propertyAmenity']


def amenities_to_csv() -> None:
    amenities = fetch_amenities_data()

    df = pd.DataFrame([j for i in amenities for j in amenities[i]['default']])
    df.sort_values(by=['category', 'id'], inplace=True)

    duplicated_idx = df[df['id'].duplicated()].index
    df.drop(columns=['url'], index=duplicated_idx, inplace=True)

    df.to_csv(amenities_fp, index=False)
    logger.info(f'Export: "{amenities_fp}"')


def main():
    amenities_to_csv()


if __name__ == '__main__':
    main()
