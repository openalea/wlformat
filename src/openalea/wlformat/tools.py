import json
from jsonschema import Draft4Validator, RefResolver
import os

here = os.path.dirname(__file__)


def validate(obj_descr, schema_name):
    """Check that the description is a valid data interface description.

    Args:
        obj_descr: (dict)
        schema_name: (str) name of object

    Returns:
        (bool) - true if description match node json schema
    """
    with open(os.path.join(here, "schema_%s.json" % schema_name), 'r') as fs:
        schema = json.load(fs)

    if here.startswith("/"):
        base_uri = "file:///%s/" % (here[1:])
    else:
        base_uri = "file:///%s/" % here
    refres = RefResolver(base_uri, schema)
    val = Draft4Validator(schema, resolver=refres)
    return val.is_valid(obj_descr)
