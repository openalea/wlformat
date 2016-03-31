from openalea.wlformat import prov_exe


def test_valid_schema():
    pdef = {
        "id": "bb060be1da2c11e5a216ace010ea24cf",
        "name": "Test Workflow Prov",
        "author": "revesansparole",
        "version": 0,
        "description": "debug purpose only",
        "workflow": "wkf60be1da2c11e5a216ace010ea24cf",
        "time_init": 0.,
        "time_end": 1.,
        "data": [
            {
                "id": "46793ee1dbdb11e5bd1eace010ea24cf",
                "type": "str",
                "value": "toto"
            },
            {
                "id": "467435d1dbdb11e599adace010ea24cf",
                "type": "int",
                "value": 0
            }
        ],
        "parameters": [
            {
                "node": 0,
                "port": "a",
                "data": "467435d1dbdb11e599adace010ea24cf"
            }
        ],
        "executions": [
            {
                "node": 0,
                "time_init": 0.,
                "time_end": 1.,
                "inputs": [
                    {
                        "port": "a",
                        "data": "46793ee1dbdb11e5bd1eace010ea24cf"
                    }
                ],
                "outputs": [
                    {
                        "port": "ret",
                        "data": "46793ee1dbdb11e5bd1eace010ea24cf"
                    }
                ]
            }
        ]
    }

    assert prov_exe.validate(pdef)
