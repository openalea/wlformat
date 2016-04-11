from openalea.wlformat.convert import graphviz


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
                "id": "nodeab8cead211e586286003089581fc"
            },
            {
                "id": "nodeab8cead211e586286003089581fc",
                "label": "mylabel"
            },
            {
                "id": "nodefailead211e586286003089581fc"
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

    txt = graphviz.export_workflow(wkf, store)
    assert "digraph" in txt
    assert "node0" in txt
    assert "node1" in txt
    assert "node2" in txt


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
                "id": "nodeab8cead211e586286003089581fc"
            }
        ],
        "links": []
    }

    store = {}
    txt = graphviz.export_workflow(wkf, store)
    assert "digraph" in txt
    assert "label=" in txt

    store = {node['id']: node}
    txt = graphviz.export_workflow(wkf, store)
    assert "digraph" in txt
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
                "label": "takapouet"
            }
        ],
        "links": []
    }

    store = {}
    txt = graphviz.export_workflow(wkf, store)
    assert "digraph" in txt
    assert "takapouet" in txt


def test_export_workflow_handle_position():
    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc"
            }
        ],
        "links": []
    }

    store = {}
    txt = graphviz.export_workflow(wkf, store)
    assert "digraph" in txt
    assert "pos=" not in txt

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "x": 0.
            }
        ],
        "links": []
    }

    store = {}
    txt = graphviz.export_workflow(wkf, store)
    assert "digraph" in txt
    assert "pos=" not in txt

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "y": 0.
            }
        ],
        "links": []
    }

    store = {}
    txt = graphviz.export_workflow(wkf, store)
    assert "digraph" in txt
    assert "pos=" not in txt

    wkf = {
        "id": "workflowead211e586286003089581fc",
        "version": 0,
        "name": "Test Workflow",
        "description": "test workflow",
        "author": "unknown",
        "nodes": [
            {
                "id": "nodeab8cead211e586286003089581fc",
                "x": 0.,
                "y": -10.
            }
        ],
        "links": []
    }

    store = {}
    txt = graphviz.export_workflow(wkf, store)
    assert "digraph" in txt
    assert "pos=" in txt
