import json
from jsonschema import Draft4Validator
import os

if os.path.exists("test"):
    sch_pth = os.path.join(os.getcwd(), "src/openalea/wlformat/")
else:
    sch_pth = os.path.join(os.path.dirname(os.getcwd()),
                           "src/openalea/wlformat/")


def test_schema_validity():
    for name in ("schema_base.json",
                 "schema_data.json",
                 "schema_node.json",
                 "schema_prov_exe.json",
                 "schema_workflow.json"):
        with open(os.path.join(sch_pth, name), 'r') as f:
            schema = json.load(f)
            Draft4Validator.check_schema(schema)
