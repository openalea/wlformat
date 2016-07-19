from copy import deepcopy
from nose.tools import assert_raises

from openalea.wlformat.prov_exe import data_produced_by, data_used_by

pdef = {
    "id": "bb060be1da2c11e5a216ace010ea24cf",
    "name": "Test Workflow Prov",
    "owner": "revesansparole",
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


def test_data_prod_raise_error_node_not_defined():
    assert_raises(IndexError, lambda: data_produced_by(pdef, 10, "ret"))


def test_data_prod_raise_error_port_not_defined():
    assert_raises(KeyError, lambda: data_produced_by(pdef, 0, "totutita"))


def test_data_prod_raise_error_if_more_than_one_execution():
    ldef = deepcopy(pdef)
    ldef["executions"].append(ldef["executions"][0])
    assert_raises(UserWarning, lambda: data_produced_by(ldef, 0, "ret"))


def test_data_prod_retrieve_data_associated_with_output_port():
    did, val = data_produced_by(pdef, 0, "ret")

    assert did == "46793ee1dbdb11e5bd1eace010ea24cf"
    assert val == "toto"


def test_data_used_raise_error_node_not_defined():
    assert_raises(IndexError, lambda: data_used_by(pdef, 10, "a"))


def test_data_used_raise_error_port_not_defined():
    assert_raises(KeyError, lambda: data_used_by(pdef, 0, "totutita"))


def test_data_used_raise_error_if_more_than_one_execution():
    ldef = deepcopy(pdef)
    ldef["executions"].append(ldef["executions"][0])
    assert_raises(UserWarning, lambda: data_used_by(ldef, 0, "a"))


def test_data_used_retrieve_data_associated_with_output_port():
    did, val = data_used_by(pdef, 0, "a")

    assert did == "46793ee1dbdb11e5bd1eace010ea24cf"
    assert val == "toto"
