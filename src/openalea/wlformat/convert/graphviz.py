"""Converter (writer only) for graphviz dot files
"""


def export_workflow(wkf, store):
    """Construct a graphviz description for a workflow.

    Args:
        wkf: (WorkflowDef)
        store: (dict of uid, def) elements definitions

    Returns:
        (dict) - workflow definition
    """
    txt = "digraph {\n"

    for ind, node in enumerate(wkf["nodes"]):
        ndef = store.get(node['id'], None)
        txt += "    node%d [" % ind

        label = node.get("label", None)
        if label is None:
            if ndef is None:
                label = "node%d" % ind
            else:
                label = ndef["name"]

        txt += 'label="%s"' % label

        x = node.get("x", None)
        y = node.get("y", None)
        if x is not None and y is not None:
            txt += ', pos="%f,%f!"' % (x, y)

        txt += ', URL="http://127.0.0.1:6543/project_content/%s"' % node['id']
        txt += "]\n"

    for link in wkf['links']:
        txt += "    node%d -> node%d" % (link['source'], link['target'])
        txt += ' [taillabel="%s"' % link['source_port']
        txt += ', headlabel="%s"]\n' % link['target_port']

    txt += "}\n"

    return txt
