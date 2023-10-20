from src.logger import get_logger
from src.typing import Acres99Dict

logger = get_logger(__name__)


async def separate_projects_srp_entity(items: list[dict]) -> tuple[list, list]:
    """Returns: (srp, project)"""
    srp, projects = [], []

    for item in items:
        if "entityType" in item.keys():
            projects.append(item)
        else:
            srp.append(item)

    return srp, projects


async def filter_batch_response(responses: list[dict]) -> Acres99Dict:
    rv = Acres99Dict(facets=responses[0]["facets"], srp=[], projects=[])

    for i in responses:
        srp, projects = await separate_projects_srp_entity(i["properties"])
        rv["srp"].extend(srp)
        rv["projects"].extend(projects)

    for i in rv.keys():
        logger.info(f"Shape of data after gathering {i}: {len(rv[i])}")

    return rv
