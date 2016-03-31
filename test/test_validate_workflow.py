import json
from jsonschema import Draft4Validator, RefResolver
import os

if os.path.exists("test"):
    sch_pth = os.path.join(os.getcwd(), "src/openalea/wlformat/")
else:
    sch_pth = os.path.join(os.path.dirname(os.getcwd()),
                           "src/openalea/wlformat/")


def test_valid_schema():
    wdef = {
        "id": "bb060be1da2c11e5a216ace010ea24cf",
        "name": "Test Workflow",
        "author": "revesansparole",
        "version": 0,
        "description": "debug purpose only",
        "nodes": [
            {
                "id": "46793ee1dbdb11e5bd1eace010ea24cf",
                "x": -50,
                "y": -140
            },
            {
                "id": "467435d1dbdb11e599adace010ea24cf",
                "label": "int"
            }
        ],
        "links": [
            {
                "source": 0,
                "source_port": "ret",
                "target": 1,
                "target_port": "a"
            }
        ]
    }

    with open(sch_pth + "schema_workflow.json", 'r') as f:
        schema = json.load(f)

    refres = RefResolver("file:///%s" % sch_pth, schema)
    val = Draft4Validator(schema, resolver=refres)
    assert val.is_valid(wdef)
    # val.validate(wdef)
