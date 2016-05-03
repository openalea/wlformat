"""Workflow helper functions.
"""
from . import tools


def validate(workflow_descr):
    """Check that the description is a valid workflow description.

    Args:
        workflow_descr: (dict)

    Returns:
        (bool) - true if description match workflow json schema
    """
    return tools.validate(workflow_descr, "workflow")
