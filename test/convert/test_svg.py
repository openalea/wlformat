from nose.tools import assert_raises

from openalea.wlformat.convert import svg


def test_export_workflow():
    node = {
        "id": "nodeab8cead211e586286003089581fc",
        "version": 0,
        "name": "some node",
        "description": "test node",
        "author": "unknown",
        "function": "func",
        "inputs": [
            {
                "default": "0",
                "interface": "int",
                "description": "some input",
                "name": "in1"
            },
            {
                "default": "1",
                "interface": "int",
                "description": "some other input",
                "name": "in2"
            }
        ],
        "outputs": [
            {
                "default": "",
                "interface": "any",
                "description": "result",
                "name": "out"
            }
        ]}

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "x": 0,
                "y": 0
            },
            {
                "id": "nodeab8cead211e586286003089581fc",
                "label": "mylabel",
                "x": 0,
                "y": 50
            },
            {
                "id": "nodefailead211e586286003089581fc",
                "x": 0,
                "y": 100
            }
        ],
        "links": [
            {
                "source": 0,
                "source_port": "out",
                "target": 2,
                "target_port": "in1"
            },
            {
                "source": 1,
                "source_port": "out",
                "target": 2,
                "target_port": "in2"
            }
        ]
    }

    store = {node['id']: node}

    txt = svg.export_workflow(wkf, store)
    assert "wkf_node_0" in txt
    assert "wkf_node_1" in txt
    assert "wkf_node_2" in txt


def test_export_workflow_raise_error_if_no_pos():
    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "label": "takapouet"
            }
        ],
        "links": []
    }

    store = {}
    assert_raises(UserWarning, lambda: svg.export_workflow(wkf, store))


def test_export_workflow_handle_missing_definitions():
    node = {
        "id": "nodeab8cead211e586286003089581fc",
        "version": 0,
        "name": "some node",
        "description": "test node",
        "author": "unknown",
        "function": "func",
        "inputs": [
            {
                "default": "0",
                "interface": "int",
                "description": "some input",
                "name": "in1"
            },
            {
                "default": "1",
                "interface": "int",
                "description": "some other input",
                "name": "in2"
            }
        ],
        "outputs": [
            {
                "default": "",
                "interface": "any",
                "description": "result",
                "name": "out"
            }
        ]}

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "x": 0,
                "y": 0
            },
            {
                "id": "nodeab8cead211e586286003089581fc",
                "x": 0,
                "y": 50
            }
        ],
        "links": [
            {
                "source": 0,
                "source_port": "out",
                "target": 1,
                "target_port": "in1"
            },
            {
                "source": 0,
                "source_port": "out",
                "target": 1,
                "target_port": "dummy"
            }

        ]
    }

    store = {}
    txt = svg.export_workflow(wkf, store)
    assert "node0" in txt
    assert "node1" in txt

    store = {node['id']: node}
    txt = svg.export_workflow(wkf, store)
    assert "wkf_link_0" in txt
    assert "wkf_link_1" in txt


def test_export_workflow_handle_label():
    node = {
        "id": "nodeab8cead211e586286003089581fc",
        "version": 0,
        "name": "some node",
        "description": "test node",
        "author": "unknown",
        "function": "func",
        "inputs": [
            {
                "default": "0",
                "interface": "int",
                "description": "some input",
                "name": "in1"
            },
            {
                "default": "1",
                "interface": "int",
                "description": "some other input",
                "name": "in2"
            }
        ],
        "outputs": [
            {
                "default": "",
                "interface": "any",
                "description": "result",
                "name": "out"
            }
        ]}

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "x": 0,
                "y": 0
            }
        ],
        "links": []
    }

    store = {}
    txt = svg.export_workflow(wkf, store)
    assert "node0" in txt

    store = {node['id']: node}
    txt = svg.export_workflow(wkf, store)
    assert "some node" in txt

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "label": "takapouet",
                "x": 0,
                "y": 0
            }
        ],
        "links": []
    }

    store = {}
    txt = svg.export_workflow(wkf, store)
    assert "takapouet" in txt


def test_export_workflow_handle_node_url():
    node = {
        "id": "nodeab8cead211e586286003089581fc",
        "version": 0,
        "name": "some node",
        "description": "test node",
        "author": "unknown",
        "function": "func",
        "url": "my_pretty_url",
        "inputs": [
            {
                "default": "0",
                "interface": "int",
                "description": "some input",
                "name": "in1"
            },
            {
                "default": "1",
                "interface": "int",
                "description": "some other input",
                "name": "in2"
            }
        ],
        "outputs": [
            {
                "default": "",
                "interface": "any",
                "description": "result",
                "name": "out"
            }
        ]}

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "x": 0,
                "y": 0
            }
        ],
        "links": []
    }

    store = {}
    txt = svg.export_workflow(wkf, store)
    assert "my_pretty_url" not in txt

    store = {node['id']: node}
    txt = svg.export_workflow(wkf, store)
    assert "my_pretty_url" in txt


def test_export_workflow_handle_interface_url():
    idef1 = {
        "id": "idef1b8cead211e586286003089581fc",
        "version": 0,
        "name": "ITest1",
        "description": "test interface1",
        "author": "unknown",
        "url": "my_pretty_url1",
        "schema": {}
    }
    idef2 = {
        "id": "idef2b8cead211e586286003089581fc",
        "version": 0,
        "name": "ITest2",
        "description": "test interface2",
        "author": "unknown",
        "url": "my_pretty_url2",
        "schema": {}
    }
    node = {
        "id": "nodeab8cead211e586286003089581fc",
        "version": 0,
        "name": "some node",
        "description": "test node",
        "author": "unknown",
        "function": "func",
        "inputs": [
            {
                "default": "0",
                "interface": "idef1b8cead211e586286003089581fc",
                "description": "some input",
                "name": "in1"
            },
            {
                "default": "1",
                "interface": "int",
                "description": "some other input",
                "name": "in2"
            }
        ],
        "outputs": [
            {
                "default": "",
                "interface": "idef2b8cead211e586286003089581fc",
                "description": "result",
                "name": "out"
            }
        ]}

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "x": 0,
                "y": 0
            }
        ],
        "links": []
    }

    store = {}
    txt = svg.export_workflow(wkf, store)
    assert "my_pretty_url1" not in txt

    store = {node['id']: node}
    txt = svg.export_workflow(wkf, store)
    assert "my_pretty_url1" not in txt

    store = {node['id']: node, idef1['id']: idef1, idef2['id']: idef2}
    txt = svg.export_workflow(wkf, store)
    assert "my_pretty_url1" in txt
    assert "my_pretty_url2" in txt


def test_export_node():
    node = {
        "id": "nodeab8cead211e586286003089581fc",
        "version": 0,
        "name": "some node",
        "description": "test node",
        "author": "unknown",
        "function": "func",
        "inputs": [
            {
                "default": "0",
                "interface": "int",
                "description": "some input",
                "name": "in1"
            },
            {
                "default": "1",
                "interface": "int",
                "description": "some other input",
                "name": "in2"
            }
        ],
        "outputs": [
            {
                "default": "",
                "interface": "any",
                "description": "result",
                "name": "out"
            }
        ]}

    store = {}

    txt = svg.export_node(node, store)
    assert node['name'] in txt
    assert "in1" in txt
    assert "in2" in txt
    assert "out" in txt


def test_export_node_handle_interface_url():
    idef1 = {
        "id": "idef1b8cead211e586286003089581fc",
        "version": 0,
        "name": "ITest1",
        "description": "test interface1",
        "author": "unknown",
        "url": "my_pretty_url1",
        "schema": {}
    }
    idef2 = {
        "id": "idef2b8cead211e586286003089581fc",
        "version": 0,
        "name": "ITest2",
        "description": "test interface2",
        "author": "unknown",
        "url": "my_pretty_url2",
        "schema": {}
    }

    node = {
        "id": "nodeab8cead211e586286003089581fc",
        "version": 0,
        "name": "some node",
        "description": "test node",
        "author": "unknown",
        "function": "func",
        "inputs": [
            {
                "default": "0",
                "interface": "idef1b8cead211e586286003089581fc",
                "description": "some input",
                "name": "in1"
            },
            {
                "default": "1",
                "interface": "int",
                "description": "some other input",
                "name": "in2"
            }
        ],
        "outputs": [
            {
                "default": "",
                "interface": "idef2b8cead211e586286003089581fc",
                "description": "result",
                "name": "out"
            }
        ]}

    store = {idef1['id']: idef1, idef2['id']: idef2}

    txt = svg.export_node(node, store)
    assert "my_pretty_url1" in txt
    assert "my_pretty_url2" in txt

