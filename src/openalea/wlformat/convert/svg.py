"""Converter (writer only) for svg files
"""
from svgwrite import Drawing


def draw_node(paper, workflow, store, node, ind):
    """Draw a single node of a workflow definition

    Args:
        paper (svgwrite.Paper):
        workflow (WorkflowDef)
        store (dict of uid, def): elements definitions
        node: current node to draw
        ind (int): index of current node

    Returns:
        None: add elements to paper in place
    """
    nw = 80
    nh = 40
    pr = 5

    nf = store.get(node['id'], None)

    if nf is not None:
        nb = max(len(nf['inputs']), len(nf['outputs']))
        nw = max(nw, pr * (nb * 4 + 4))

    g = paper.add(paper.g())
    g.translate(node['x'], node['y'])
    if nf is not None and 'url' in nf:
        link = g.add(paper.a(href=nf['url'], target='_top'))
    else:
        link = g

    link.attribs['id'] = "wkf_node_%d" % ind

    # background
    bg = paper.rect((-nw / 2, -nh / 2), (nw, nh), rx=5, ry=5, stroke_width=1)
    link.add(bg)
    if nf is None:
        bg.stroke('#ff8080')
        bg.fill("url(#bg_failed)")
    else:
        bg.stroke('#808080')
        bg.fill("url(#bg_loaded)")

    # label
    label_txt = None
    if 'label' in node:
        label_txt = node['label']

    if label_txt is None:
        if nf is None:
            label_txt = "node%d" % ind
        else:
            label_txt = nf['name']

    style = 'font-size: 18px; font-family: verdana; text-anchor: middle'
    frag = paper.tspan(label_txt, dy=[5])
    label = paper.text("", style=style, fill='#000000')
    label.add(frag)
    link.add(label)

    # ports
    if nf is not None:
        nb = len(nf['inputs'])
        py = -nh / 2
        for i, pdef in enumerate(nf['inputs']):
            px = i * pr * 4 - (nb - 1) * 2 * pr
            port = paper.circle((px, py), pr, stroke='#000000', stroke_width=1)
            port.fill("url(#in_port)")
            pid = "wkf_node_%d_input_%s" % (ind, pdef['name'])

            idef = store.get(pdef['interface'], None)
            if idef is not None and 'url' in idef:
                link = g.add(paper.a(href=idef['url'], target='_top'))
                link.attribs['id'] = pid
                link.add(port)
            else:
                port.attribs['id'] = pid
                g.add(port)

        nb = len(nf['outputs'])
        py = nh / 2
        for i, pdef in enumerate(nf['outputs']):
            px = i * pr * 4 - (nb - 1) * 2 * pr
            port = paper.circle((px, py), pr, stroke='#000000', stroke_width=1)
            port.fill("url(#out_port)")
            pid = "wkf_node_%d_output_%s" % (ind, pdef['name'])

            idef = store.get(pdef['interface'], None)
            if idef is not None and 'url' in idef:
                link = g.add(paper.a(href=idef['url'], target='_top'))
                link.attribs['id'] = pid
                link.add(port)
            else:
                port.attribs['id'] = pid
                g.add(port)


def port_index(ports, port_name):
    """Find index of named port

    Args:
        ports (list of ports):
        port_name (str): local id of port

    Returns:
        (int): index of port or None
    """
    for i, port in enumerate(ports):
        if port['name'] == port_name:
            return i

    return None


def draw_link(paper, workflow, store, link, ind):
    """Draw a single node of a workflow definition

    Args:
        paper (svgwrite.Paper):
        workflow (WorkflowDef)
        store (dict of uid, def): elements definitions
        link (): actual link to draw
        ind (int): index of current link in list of links

    Returns:
        None: add elements to paper in place
    """
    nh = 40
    pr = 5

    src = workflow['nodes'][link['source']]
    src_x = src['x']
    src_y = src['y']
    nf = store.get(src['id'], None)
    if nf is not None:
        i = port_index(nf['outputs'], link['source_port'])
        if i is not None:
            nb = len(nf['outputs'])
            src_x += i * pr * 4 - (nb - 1) * 2 * pr
            src_y += nh / 2.

    tgt = workflow['nodes'][link['target']]
    tgt_x = tgt['x']
    tgt_y = tgt['y']

    nf = store.get(tgt['id'], None)
    if nf is not None:
        i = port_index(nf['inputs'], link['target_port'])
        if i is not None:
            nb = len(nf['inputs'])
            tgt_x += i * pr * 4 - (nb - 1) * 2 * pr
            tgt_y -= nh / 2.

    pth = paper.polyline([(src_x, src_y), (tgt_x, tgt_y)],
                         stroke='#000000',
                         stroke_width=1,
                         id="wkf_link_%d" % ind)
    paper.add(pth)


def export_workflow(workflow, store, size=None):
    """Construct a SVG description for a workflow

    Args:
        workflow (WorkflowDef)
        store (dict of uid, def): elements definitions
        size (int, int): size of drawing in pixels

    Returns:
        (str) - SVG description of workflow
    """
    # check that each node has a position
    for node in workflow['nodes']:
        if 'x' not in node or 'y' not in node:
            raise UserWarning("need to position workflow first")

    if size is None:
        size = (600, 600)

    nw = 80
    nh = 40
    pr = 5
    padding = 20

    paper = Drawing("workflow.svg", size, id="repr")

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="bg_loaded")
    lg.add_stop_color(0, color='#8c8cff')
    lg.add_stop_color(1, color='#c8c8c8')
    paper.defs.add(lg)

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="bg_failed")
    lg.add_stop_color(0, color='#ff8cff')
    lg.add_stop_color(1, color='#c8c8c8')
    paper.defs.add(lg)

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="in_port")
    lg.add_stop_color(0, color='#3333ff')
    lg.add_stop_color(1, color='#2222ff')
    paper.defs.add(lg)

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="out_port")
    lg.add_stop_color(0, color='#ffff33')
    lg.add_stop_color(1, color='#9a9a00')
    paper.defs.add(lg)

    for i, link in enumerate(workflow['links']):
        draw_link(paper, workflow, store, link, i)

    for i, node in enumerate(workflow['nodes']):
        draw_node(paper, workflow, store, node, i)

    xmin = min(node['x'] for node in workflow['nodes']) - nw / 2 - padding
    xmax = max(node['x'] for node in workflow['nodes']) + nw / 2 + padding
    ymin = min(node['y'] for node in workflow['nodes']) - nh / 2 - pr - padding
    ymax = max(node['y'] for node in workflow['nodes']) + nh / 2 + pr + padding

    w = float(size[0])
    h = float(size[1])
    xratio = (xmax - xmin) / w
    yratio = (ymax - ymin) / h
    if xratio > yratio:
        xsize = int(xratio * w)
        ysize = int(xratio * h)
        ymin -= (ysize - (ymax - ymin)) / 2
    else:
        xsize = int(yratio * w)
        ysize = int(yratio * h)
        xmin -= (xsize - (xmax - xmin)) / 2

    paper.viewbox(xmin, ymin, xsize, ysize)

    return paper.tostring()
