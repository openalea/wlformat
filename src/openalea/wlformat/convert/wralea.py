"""Converter (reader only) for wralea files."""

from datetime import datetime
from uuid import uuid1


def get_interface_by_name(store, name):
    """Find an interface in store from its name.

    Args:
        store: (dict of uid, def)
        name: (str) name of interface

    Returns:
        (idef|None) - returns None if no such interface exists
    """
    for typ, idef in store.values():
        if typ == "data":
            if idef["name"] == name:
                return idef

    return None


def register_interface(store, name, author="unknown"):
    """Register an interface in store whose name is given.

    Args:
        store (dict of uid, def):
        name (str): name of interface
        author (str): owner of interface definition

    Returns:
        (idef) - interface definition
    """
    uid = uuid1().hex
    idef = dict(id=uid,
                name=name,
                description="",
                owner=author,
                version=0,
                schema={},
                ancestors=[])

    store[uid] = ('data', idef)

    return idef


def get_node_by_func_desc(store, func_desc):
    """Find a node in store whose name is pkg: func_name.

    Args:
        store: (dict of uid, ndef)
        func_desc: (str, str) pkg, func_name

    Returns:
        (ndef|None) - returns None if no such node exists
    """
    name = "%s: %s" % func_desc
    for typ, ndef in store.values():
        if typ == "node":
            if ndef["name"] == name:
                return ndef

    return None


def register_node(store, func_desc):
    """Register a node in store whose name is pkg: func_name.

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
                owner="unknown",
                version=0,
                function="null",
                inputs=[],
                outputs=[])

    store[uid] = ('node', ndef)

    return ndef


def convert_node(nf, store, pkgname):
    """Convert a NodeFactory into a node file.

    Warnings: modify store in place to add unregistered interfaces

    Args:
        nf: (NodeFactory)
        store: (dict of uid, def) elements definitions
        pkgname: (str) name of openalea package

    Returns:
        (dict) - workflow definition
    """
    try:
        uid = nf.uid
    except AttributeError:
        uid = uuid1().hex

    name = "%s: %s" % (pkgname, nf.name)
    author = nf.get_authors()
    if author.endswith(" (wralea authors)"):
        author = author[:-17]
    if len(author) == 0:
        author = "unknown"

    ndef = dict(id=uid,
                name=name,
                description=nf.description,
                owner=author,
                created=datetime.now().isoformat(),
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
        idef = get_interface_by_name(store, iname)
        if idef is None:
            msg = "unable to find proper def for interface '%s'" % iname
            raise UserWarning(msg)

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
        idef = get_interface_by_name(store, iname)
        if idef is None:
            msg = "unable to find proper def for interface '%s'" % iname
            raise UserWarning(msg)

        pdef = dict(name=port.get('name', 'out'),
                    interface=idef['id'],
                    default=str(port.get("value", "")),
                    description=port.get("descr", ""))
        ndef['outputs'].append(pdef)

    return ndef


def convert_workflow(cnf, store):
    """Construct a workflow definition from a composite node factory.

    Warnings: modify store in place

    Warnings: do not handle CompositeNodes as in workflows
              with connections to either __in__ or __out__

    Args:
        cnf: (CompositeNodeFactory)
        store: (dict of uid, def) elements definitions

    Returns:
        (dict) - workflow definition
    """
    for link in cnf.connections.values():
        src, ipid, tgt, opid = link
        if src == '__in__' or tgt == '__out__':
            return None

    try:
        uid = cnf.uid
    except AttributeError:
        uid = uuid1().hex

    author = cnf.get_authors()
    if author.endswith(" (wralea authors)"):
        author = author[:-17]
    if len(author) == 0:
        author = "unknown"

    wdef = dict(id=uid,
                name=cnf.name,
                description=cnf.description,
                owner=author,
                created=datetime.now().isoformat(),
                version=0,
                nodes=[],
                links=[])

    ntrans = {}
    for nid, func_desc in cnf.elt_factory.items():
        ntrans[nid] = len(wdef['nodes'])
        ndef = get_node_by_func_desc(store, func_desc)
        if ndef is None:
            raise UserWarning("unknown node %s: %s" % func_desc)

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

    for link in cnf.connections.values():
        src, opid, tgt, ipid = link
        # find port names instead of indexes
        src_typ, src_def = store[wdef['nodes'][ntrans[src]]['id']]
        src_pname = src_def['outputs'][opid]['name']
        tgt_typ, tgt_def = store[wdef['nodes'][ntrans[tgt]]['id']]
        tgt_pname = tgt_def['inputs'][ipid]['name']

        new_link = dict(source=ntrans[src],
                        source_port=src_pname,
                        target=ntrans[tgt],
                        target_port=tgt_pname)
        wdef['links'].append(new_link)

    return wdef
