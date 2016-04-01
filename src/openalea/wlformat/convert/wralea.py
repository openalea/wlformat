"""Converter (reader only) for wralea files
"""
from uuid import uuid1


def find_wralea_interface(store, name):
    """Find an interface in store from its name

    Args:
        store: (dict of uid, def)
        name: (str) name of interface

    Returns:
        (idef|None) - returns None if no such interface exists
    """
    for uid, (typ, idef) in store.items():
        if typ == "data":
            if idef["name"] == name:
                return idef

    return None


def register_wralea_interface(store, name):
    """Register an interface in store whose name is given

    Args:
        store: (dict of uid, def)
        name: (str) name of interface

    Returns:
        (idef) - interface definition
    """
    uid = uuid1().hex
    idef = dict(id=uid,
                name=name,
                description="",
                author="unknown",
                version=0,
                schema={},
                ancestors=[])

    store[uid] = ('data', idef)

    return idef


def find_wralea_node(store, func_desc):
    """Find a node in store whose name is pkg: func_name

    Args:
        store: (dict of uid, ndef)
        func_desc: (str, str) pkg, func_name

    Returns:
        (ndef|None) - returns None if no such node exists
    """
    name = "%s: %s" % func_desc
    for uid, (typ, ndef) in store.items():
        if typ == "node":
            if ndef["name"] == name:
                return ndef

    return None


def register_wralea_node(store, func_desc):
    """Register a node in store whose name is pkg: func_name

    Args:
        store: (dict of uid, ndef)
        func_desc: (str, str) pkg, func_name

    Returns:
        (ndef) - node definition
    """
    uid = uuid1().hex
    ndef = dict(id=uid,
                name="%s: %s" % func_desc,
                description="%s: %s" % func_desc,
                author="unknown",
                version=0,
                function="null",
                inputs=[],
                outputs=[])

    store[uid] = ('node', ndef)

    return ndef


def import_node(nf, store, pkgname):
    """Convert a NodeFactory into a node file.

    Warnings: modify store in place to add unregistered interfaces

    Args:
        nf: (NodeFactory)
        store: (dict of uid, def) elements definitions
        pkgname: (str) name of openalea package

    Returns:
        (dict) - workflow definition
    """
    name = "%s: %s" % (pkgname, nf.name)

    ndef = dict(id=uuid1().hex,
                name=name,
                description=nf.description,
                author="unknown",
                version=0,
                function="py:%s#%s" % (nf.nodemodule_name,
                                       nf.nodeclass_name),
                inputs=[],
                outputs=[])

    inputs = nf.inputs
    if inputs is None:
        inputs = []

    for port in inputs:
        iname = str(port.get('interface', "any"))
        idef = find_wralea_interface(store, iname)
        if idef is None:
            idef = register_wralea_interface(store, iname)

        pdef = dict(name=port.get('name', 'in'),
                    interface=idef['id'],
                    default=str(port.get("value", "")),
                    description=port.get("descr", ""))
        ndef['inputs'].append(pdef)

    outputs = nf.outputs
    if outputs is None:
        outputs = []

    for port in outputs:
        iname = str(port.get('interface', "any"))
        idef = find_wralea_interface(store, iname)
        if idef is None:
            idef = register_wralea_interface(store, iname)

        pdef = dict(name=port.get('name', 'out'),
                    interface=idef['id'],
                    default=str(port.get("value", "")),
                    description=port.get("descr", ""))
        ndef['outputs'].append(pdef)

    return ndef


def import_workflow(cnf, store):
    """Construct a workflow definition from a composite node factory

    Warnings: modify store in place

    Args:
        cnf: (CompositeNodeFactory)
        store: (dict of uid, def) elements definitions

    Returns:
        (dict) - workflow definition
    """
    wdef = dict(id=uuid1().hex,
                name=cnf.name,
                description=cnf.description,
                author="unknown",
                version=0,
                nodes=[],
                links=[])

    ntrans = {}
    for nid, func_desc in cnf.elt_factory.items():
        ntrans[nid] = len(wdef['nodes'])
        ndef = find_wralea_node(store, func_desc)
        if ndef is None:
            ndef = register_wralea_node(store, func_desc)

        node = dict(id=ndef['id'])
        # data
        data = cnf.elt_data.get(nid, {})
        block = data.get('block', False)
        if block:
            node['block'] = True

        caption = data.get('caption', "")
        if len(caption) > 0:
            node['label'] = caption

        delay = data.get('delay', 0)
        if delay > 0:
            node['delay'] = delay

        hide = data.get('hide', False)
        if hide:
            node['hide'] = True

        lazy = data.get('lazy', True)
        if not lazy:
            node['lazy'] = False

        posx = data.get('posx', None)
        if posx is not None:
            node['x'] = posx
        posy = data.get('posy', None)
        if posy is not None:
            node['y'] = posy

        priority = data.get('priority', 0)
        if priority > 0:
            node['priority'] = priority

        use_user_color = data.get('use_user_color', False)
        if use_user_color:
            node['use_user_color'] = True

        user_application = data.get('user_application', None)
        if user_application is not None:
            node['user_application'] = user_application

        user_color = data.get('user_color', None)
        if user_color is not None:
            node['user_color'] = user_color

        data = cnf.elt_ad_hoc.get(nid, {})
        if 'x' not in node:
            pos = data.get('position', None)
            if pos is not None:
                node['x'], node['y'] = pos

        if 'user_color' not in node:
            user_color = data.get('userColor', None)
            if user_color is not None:
                node['user_color'] = user_color

        if 'use_user_color' not in node:
            use_user_color = data.get('useUserColor', False)
            if use_user_color:
                node['use_user_color'] = use_user_color

        wdef['nodes'].append(node)

    for lid, link in cnf.connections.items():
        src, ipid, tgt, opid = link
        new_link = dict(source=ntrans[src],
                        source_port=str(ipid),
                        target=ntrans[tgt],
                        target_port=str(opid))
        wdef['links'].append(new_link)

    return wdef
