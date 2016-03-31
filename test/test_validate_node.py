import json
from jsonschema import Draft4Validator, RefResolver
import os

if os.path.exists("test"):
    sch_pth = os.path.join(os.getcwd(), "src/openalea/wlformat/")
else:
    sch_pth = os.path.join(os.path.dirname(os.getcwd()),
                           "src/openalea/wlformat/")


def test_valid_schema():
    ndef = {
        "id": "4675bc70dbdb11e5b310ace010ea24cf",
        "name": "plus",
        "description": "Add two numbers together",
        "author": "unknown",
        "version": 0,
        "function": "sample_project.nodes:plus",
        "inputs": [
            {
                "interface": "int",
                "default": "0",
                "description": "left operand",
                "name": "a"
            },
            {
                "interface": "int",
                "default": "0",
                "description": "right operand",
                "name": "b"
            }
        ],
        "outputs": [
            {
                "interface": "int",
                "description": "result of addition",
                "name": "ret"
            }
        ]
    }

    with open(sch_pth + "schema_node.json", 'r') as f:
        schema = json.load(f)

    refres = RefResolver("file:///%s" % sch_pth, schema)
    val = Draft4Validator(schema, resolver=refres)
    assert val.is_valid(ndef)
    # val.validate(ndef)
