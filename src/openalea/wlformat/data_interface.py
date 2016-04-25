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
    print "HERE3", here
    with open(os.path.join(here, "schema_data.json"), 'r') as f:
        schema = json.load(f)

    base_uri = "file:///%s/" % (here[1:])
    print "BASE_URI", base_uri
    refres = RefResolver(base_uri, schema)
    val = Draft4Validator(schema, resolver=refres)
    return val.is_valid(data_descr)
