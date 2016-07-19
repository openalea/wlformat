from openalea.wlformat import node


def test_valid_schema():
    ndef = {
        "id": "4675bc70dbdb11e5b310ace010ea24cf",
        "name": "plus",
        "description": "Add two numbers together",
        "owner": "unknown",
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

    assert node.validate(ndef)
