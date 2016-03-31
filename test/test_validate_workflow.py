from openalea.wlformat import workflow


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

    assert workflow.validate(wdef)
