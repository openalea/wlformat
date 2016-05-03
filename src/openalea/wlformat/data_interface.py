import tools


def validate(data_descr):
    """Check that the description is a valid data interface description.

    Args:
        data_descr: (dict)

    Returns:
        (bool) - true if description match node json schema
    """
    return tools.validate(data_descr, "data")
