import json
from jsonschema import Draft4Validator, RefResolver
import os


here = os.path.dirname(__file__)


def validate(node_descr):
    """Check that the description is a valid workflow node description

    Args:
        node_descr: (dict)

    Returns:
        (bool) - true if description match node json schema
    """
    with open(os.path.join(here, "schema_node.json"), 'r') as f:
        schema = json.load(f)

    refres = RefResolver("file:///%s/" % here, schema)
    print "here", here
    val = Draft4Validator(schema, resolver=refres)
    return val.is_valid(node_descr)
