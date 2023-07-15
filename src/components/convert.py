"""
Convert the Response JSON into Acres99 readable dict.
"""

from typing import Any

from src.core.logger import get_logger

logger = get_logger(__name__)


def separate_projects_srp_entity(
    items: list[dict[str, Any]],
) -> tuple[list, list]:
    """ Returns: (srp, project) """
    srp, projects = [], []

    for item in items:
        if 'entityType' in item.keys():
            projects.append(item)
        else:
            srp.append(item)

    return srp, projects


def convert_to_acres99_dict(d: dict) -> dict[str, Any]:
    srp, projects = separate_projects_srp_entity(d['properties'])

    result = {
        'facets': d['facets'],
        'srp': srp,
        'projects': projects,
    }

    for i in result.keys():
        logger.info(f'{i}: {len(result[i])}')

    return result
