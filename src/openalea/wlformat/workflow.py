import json
from jsonschema import Draft4Validator, RefResolver
import os


here = os.path.dirname(__file__)


def validate(workflow_descr):
    """Check that the description is a valid workflow description

    Args:
        workflow_descr: (dict)

    Returns:
        (bool) - true if description match workflow json schema
    """
    with open(os.path.join(here, "schema_workflow.json"), 'r') as f:
        schema = json.load(f)

    refres = RefResolver("file:///%s/" % here, schema)
    val = Draft4Validator(schema, resolver=refres)
    return val.is_valid(workflow_descr)
