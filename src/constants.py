from pathlib import Path

FACETS_DIR = Path("data/facets")
PROJECTS_CSV_PATH = Path("data/projects.csv")
SRP_CSV_PATH = Path("data/srp.csv")
SRP_COLUMNS_PATH = Path("data/srp_columns.json")

AMENITIES_PATH = Path("data/facets/AMENITIES.csv")
CITY_W_ID_PATH = Path("data/city_w_id.json")

BASE_REQUESTS_PATH = Path("base.requests.json")
MAIN_REQUESTS_PATH = Path("requests.json")

REQUEST_HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/118.0.0.0 Safari/537.36"
    )
}
