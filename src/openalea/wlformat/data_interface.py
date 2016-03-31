import json
from jsonschema import Draft4Validator, RefResolver
import os


here = os.path.dirname(__file__)


def validate(data_descr):
    """Check that the description is a valid data interface description

    Args:
        data_descr: (dict)

    Returns:
        (bool) - true if description match node json schema
    """
    with open(os.path.join(here, "schema_data.json"), 'r') as f:
        schema = json.load(f)

    refres = RefResolver("file:///%s/" % here, schema)
    print "here", here
    val = Draft4Validator(schema, resolver=refres)
    return val.is_valid(data_descr)
