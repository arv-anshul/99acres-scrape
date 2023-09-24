"""
Convert the Response JSON into Acres99Dict type.
"""

from typing import Any

from src.core.logger import get_logger
from src.typing import Acres99Dict

logger = get_logger(__name__)


async def separate_projects_srp_entity(
    items: list[dict[str, Any]],
) -> tuple[list, list]:
    """Returns: (srp, project)"""
    srp, projects = [], []

    for item in items:
        if 'entityType' in item.keys():
            projects.append(item)
        else:
            srp.append(item)

    return srp, projects


async def convert_to_acres99_dict(d: dict) -> Acres99Dict:
    srp, projects = await separate_projects_srp_entity(d['properties'])
    result = Acres99Dict(facets=d['facets'], srp=srp, projects=projects)

    for i in result.keys():
        logger.info(f'{i}: {len(result[i])}')

    return result


async def concat_responses(responses: list[Acres99Dict]) -> Acres99Dict:
    if not responses:
        raise ValueError('Empty responses passed.')

    rv = Acres99Dict(
        facets=responses[0]['facets'],
        srp=[j for i in responses for j in i['srp']],
        projects=[j for i in responses for j in i['projects']],
    )

    for i in rv.keys():
        logger.info(f'Length after concatenated {i}: {len(rv[i])}')

    return rv
