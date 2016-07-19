"""Workflow execution provenance helper functions.
"""
from . import tools


def validate(prov_descr):
    """Check that the description is a valid execution provenance description.

    Args:
        prov_descr: (dict)

    Returns:
        (bool) - true if description match node json schema
    """
    return tools.validate(prov_descr, "prov_exe")


def data_produced_by(prov_descr, node_index, port_name):
    """Retrieve data produced by a given process.

    Raises: UserWarning if the process has been executed more
            then once.

    Args:
        prov_descr (dict): a valid provenance definition
        node_index (int): index of node in workflow
        port_name (str): name of output port to look for data

    Returns:
        (str, any): tuple data id, actual value of the data
    """
    node_executions = [i for i, exe in enumerate(prov_descr["executions"])
                       if exe["node"] == node_index]
    if len(node_executions) == 0:
        raise IndexError("node %d has never been evaluated" % node_index)

    if len(node_executions) > 1:
        msg = "node %d has been executed more than once" % node_index
        raise UserWarning(msg)

    exe_ind, = node_executions
    outputs = prov_descr["executions"][exe_ind]["outputs"]

    for output in outputs:
        if output["port"] == port_name:
            did = output["data"]
            for data_descr in prov_descr["data"]:
                if data_descr['id'] == did:
                    return did, data_descr["value"]

            raise UserWarning("Provenance file is not valid")

    raise KeyError("port %s is not defined" % port_name)


def data_used_by(prov_descr, node_index, port_name):
    """Retrieve data used by a given process.

    Raises: UserWarning if the process has been executed more
            then once.

    Args:
        prov_descr (dict): a valid provenance definition
        node_index (int): index of node in workflow
        port_name (str): name of input port to look for data

    Returns:
        (str, any): tuple data id, actual value of the data
    """
    node_executions = [i for i, exe in enumerate(prov_descr["executions"])
                       if exe["node"] == node_index]
    if len(node_executions) == 0:
        raise IndexError("node %d has never been evaluated" % node_index)

    if len(node_executions) > 1:
        msg = "node %d has been executed more than once" % node_index
        raise UserWarning(msg)

    exe_ind, = node_executions
    inputs = prov_descr["executions"][exe_ind]["inputs"]

    for input in inputs:
        if input["port"] == port_name:
            did = input["data"]
            for data_descr in prov_descr["data"]:
                if data_descr['id'] == did:
                    return did, data_descr["value"]

            raise UserWarning("Provenance file is not valid")

    raise KeyError("port %s is not defined" % port_name)
