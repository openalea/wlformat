import tools


def validate(node_descr):
    """Check that the description is a valid workflow node description

    Args:
        node_descr: (dict)

    Returns:
        (bool) - true if description match node json schema
    """
    return tools.validate(node_descr, "node")
