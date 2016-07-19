from openalea.wlformat import data_interface


def test_valid_schema():
    ddef = {
        "id": "url12345678912345678945612358794",
        "name": "url",
        "owner": "revesansparole",
        "version": 0,
        "description": "Url type of data",
        "schema": {
            "type": "string"
        },
        "ancestors": []
    }

    data_interface.validate(ddef)
