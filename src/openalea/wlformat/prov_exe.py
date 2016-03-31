import json
from jsonschema import Draft4Validator, RefResolver
import os


here = os.path.dirname(__file__)


def validate(prov_descr):
    """Check that the description is a valid workflow
    execution provenance description.

    Args:
        prov_descr: (dict)

    Returns:
        (bool) - true if description match node json schema
    """
    with open(os.path.join(here, "schema_prov_exe.json"), 'r') as f:
        schema = json.load(f)

    refres = RefResolver("file:///%s/" % here, schema)
    val = Draft4Validator(schema, resolver=refres)
    return val.is_valid(prov_descr)
