import tools


def validate(prov_descr):
    """Check that the description is a valid workflow
    execution provenance description.

    Args:
        prov_descr: (dict)

    Returns:
        (bool) - true if description match node json schema
    """
    return tools.validate(prov_descr, "prov_exe")
