import json
from jsonschema import Draft4Validator, RefResolver
import os

if os.path.exists("test"):
    sch_pth = os.path.join(os.getcwd(), "src/openalea/wlformat/")
else:
    sch_pth = os.path.join(os.path.dirname(os.getcwd()),
                           "src/openalea/wlformat/")


def test_valid_schema():
    ddef = {
        "id": "url12345678912345678945612358794",
        "name": "url",
        "author": "revesansparole",
        "version": 0,
        "description": "Url type of data",
        "schema": {
            "type": "string"
        },
        "ancestors": []
    }

    with open(sch_pth + "schema_data.json", 'r') as f:
        schema = json.load(f)

    refres = RefResolver("file:///%s" % sch_pth, schema)
    val = Draft4Validator(schema, resolver=refres)
    assert val.is_valid(ddef)
    # val.validate(ddef)
