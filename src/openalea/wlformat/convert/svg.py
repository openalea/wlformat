"""Converter (writer only) for svg files."""
from svgwrite import Drawing

node_width = 60
# node_height = 30
port_radius = 4
node_padding = 5

label_font = "courier"
label_font_size = 12
port_font_size = 10

draw_padding = 20


def string_size(txt, font_size):
    """Average length of txt in pixels

    Args:
        txt (str): text
        font_size (int): size of font in pixels

    Returns:
        (float)
    """
    return len(txt) * font_size * 0.8


def sanitize(name):
    """Remove troubling elements from name

    Args:
        name (str): the text to transform

    Returns:
        (str): same text without spaces, (, )
    """
    san = name.replace(" ", "")
    san = san.replace("(", "")
    san = san.replace(")", "")
    return san


def compute_node_width(nf, label, port_spacing):
    """Compute minimal width of node

    Args:
        nf (dict): node definition
        label (str): label used for this node
        port_spacing (int): spacing in pixels between two ports

    Returns:
        (int): size in pixels
    """
    label_size = string_size(label, label_font_size)

    nb = max(len(nf['inputs']), len(nf['outputs']))
    nw = max(label_size, (nb - 1) * port_spacing + 2 * port_radius)
    return nw + 2 * node_padding


def draw_node(paper, workflow, store, node, ind):
    """Draw a single node of a workflow definition.

    Args:
        paper (svgwrite.Paper):
        workflow (WorkflowDef)
        store (dict of uid, def): elements definitions
        node: current node to draw
        ind (int): index of current node

    Returns:
        (tuple of int): bounding box of drawn element
    """
    del workflow
    nf = store.get(node['id'], None)

    # label
    label_txt = None
    if 'label' in node:
        label_txt = node['label']

    if label_txt is None:
        if nf is None:
            label_txt = "node%d" % ind
        else:
            label_txt = nf['name']

    # node size
    pr = port_radius
    pspace = 4 * pr
    if nf is None:
        nw = node_width
    else:
        nw = compute_node_width(nf, label_txt, pspace)

    nh = label_font_size + 2 * pr + (2 * node_padding) * 0.5

    # draw
    g = paper.add(paper.g())
    g.translate(node['x'], node['y'])
    if nf is not None and 'url' in nf:
        link = g.add(paper.a(href=nf['url'], target='_top'))
    else:
        link = g

    link.attribs['id'] = "wkf_node_%d" % ind

    # background
    bg = paper.rect((-nw / 2, -nh / 2), (nw, nh),
                    rx=node_padding, ry=node_padding,
                    stroke_width=1)
    link.add(bg)
    if nf is None:
        bg.stroke('#ff8080')
        bg.fill("url(#bg_failed)")
    else:
        bg.stroke('#808080')
        bg.fill("url(#bg_loaded)")

    # label
    style = ('font-size: %dpx; font-family: %s; '
             'text-anchor: middle' % (label_font_size, label_font))
    frag = paper.tspan(label_txt, dy=[label_font_size // 3])
    label = paper.text("", style=style, fill='#000000')
    label.add(frag)
    link.add(label)

    # ports
    if nf is not None:
        nb = len(nf['inputs'])
        py = -nh / 2
        for i, pdef in enumerate(nf['inputs']):
            px = i * pspace - pspace * (nb - 1) / 2
            port = paper.circle((px, py), pr, stroke='#000000', stroke_width=1)
            port.fill("url(#in_port)")
            pid = "wkf_node_%d_input_%s" % (ind, sanitize(pdef['name']))

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
            px = i * pspace - pspace * (nb - 1) / 2
            port = paper.circle((px, py), pr, stroke='#000000', stroke_width=1)
            port.fill("url(#out_port)")
            pid = "wkf_node_%d_output_%s" % (ind, sanitize(pdef['name']))

            idef = store.get(pdef['interface'], None)
            if idef is not None and 'url' in idef:
                link = g.add(paper.a(href=idef['url'], target='_top'))
                link.attribs['id'] = pid
                link.add(port)
            else:
                port.attribs['id'] = pid
                g.add(port)

    bb = (node['x'] - nw / 2., node['y'] - nh / 2. - pr,
          node['x'] + nw / 2., node['y'] + nh / 2. + pr)
    return bb


def port_index(ports, port_name):
    """Find index of named port.

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
    """Draw a single node of a workflow definition.

    Args:
        paper (svgwrite.Paper):
        workflow (WorkflowDef)
        store (dict of uid, def): elements definitions
        link (): actual link to draw
        ind (int): index of current link in list of links

    Returns:
        None: add elements to paper in place
    """
    pr = port_radius
    pspace = 4 * pr
    nh = label_font_size + 2 * pr + (2 * node_padding) * 0.5  # see above

    src = workflow['nodes'][link['source']]
    src_x = src['x']
    src_y = src['y']
    nf = store.get(src['id'], None)
    if nf is not None:
        i = port_index(nf['outputs'], link['source_port'])
        if i is not None:
            nb = len(nf['outputs'])
            src_x += i * pspace - pspace * (nb - 1) / 2
            src_y += nh / 2.

    tgt = workflow['nodes'][link['target']]
    tgt_x = tgt['x']
    tgt_y = tgt['y']

    nf = store.get(tgt['id'], None)
    if nf is not None:
        i = port_index(nf['inputs'], link['target_port'])
        if i is not None:
            nb = len(nf['inputs'])
            tgt_x += i * pspace - pspace * (nb - 1) / 2
            tgt_y -= nh / 2.

    pth = paper.polyline([(src_x, src_y), (tgt_x, tgt_y)],
                         stroke='#000000',
                         stroke_width=1,
                         id="wkf_link_%d" % ind)
    paper.add(pth)


def export_workflow(workflow, store, size=None):
    """Construct a SVG description for a workflow.

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

    # draw
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

    bbs = []
    for i, node in enumerate(workflow['nodes']):
        bb = draw_node(paper, workflow, store, node, i)
        bbs.append(bb)

    # reformat whole drawing to fit screen
    xmin = min(bb[0] for bb in bbs) - draw_padding
    xmax = max(bb[2] for bb in bbs) + draw_padding
    ymin = min(bb[1] for bb in bbs) - draw_padding
    ymax = max(bb[3] for bb in bbs) + draw_padding

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

    return paper.tostring(), (xmin, ymin, xsize, ysize)


def export_node(node, store, size=None):
    """Construct a SVG description for a workflow node.

    Args:
        node (NodeDef)
        store (dict of uid, def): elements definitions
        size (int, int): size of drawing in pixels

    Returns:
        (str) - SVG description of workflow node
    """
    # pr = 15

    # node size
    pr = port_radius
    pspace = pr * 9
    nw = compute_node_width(node, node['name'], pspace)
    nh = label_font_size + 2 * pr + 2 * port_font_size + 2 + (2 * node_padding)

    # draw
    if size is None:
        size = (600, 600)

    paper = Drawing("workflow_node.svg", size, id="repr")

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="in_port")
    lg.add_stop_color(0, color='#3333ff')
    lg.add_stop_color(1, color='#2222ff')
    paper.defs.add(lg)

    lg = paper.linearGradient((0.5, 0), (0.5, 1.), id="out_port")
    lg.add_stop_color(0, color='#ffff33')
    lg.add_stop_color(1, color='#9a9a00')
    paper.defs.add(lg)

    # body
    g = paper.add(paper.g())

    # background
    lg = paper.linearGradient((0.5, 0), (0.5, 1.))
    lg.add_stop_color(0, color='#8c8cff')
    lg.add_stop_color(1, color='#c8c8c8')
    paper.defs.add(lg)

    bg = paper.rect((-nw / 2, -nh / 2), (nw, nh),
                    rx=node_padding, ry=node_padding,
                    stroke_width=1)
    bg.stroke('#808080')
    bg.fill(lg)
    g.add(bg)

    # label
    style = ('font-size: %dpx; font-family: %s; '
             'text-anchor: middle' % (label_font_size, label_font))
    frag = paper.tspan(node['name'], dy=[label_font_size // 3])
    label = paper.text("", style=style, fill='#000000')
    label.add(frag)
    g.add(label)

    # ports
    port_style = ('font-size: %dpx; ' % port_font_size +
                  'font-family: %s; ' % label_font)
    onstyle = port_style + 'text-anchor: end'
    instyle = port_style + 'text-anchor: start'
    istyle = port_style + 'text-anchor: middle'
    nb = len(node['inputs'])
    py = -nh / 2
    for i, pdef in enumerate(node['inputs']):
        px = i * pspace - pspace * (nb - 1) / 2
        pg = g.add(paper.g())
        pg.translate(px, py)
        idef = store.get(pdef['interface'], None)
        if idef is not None and 'url' in idef:
            link = pg.add(paper.a(href=idef['url'], target='_top'))
        else:
            link = pg

        port = paper.circle((0, 0), pr, stroke='#000000', stroke_width=1)
        port.fill("url(#in_port)")
        link.add(port)
        # port name
        frag = paper.tspan(pdef['name'], dy=[-2 * pr])
        label = paper.text("", style=instyle, fill='#000000')
        label.rotate(-45)
        label.add(frag)
        pg.add(label)
        # port interface
        if idef is None:
            itxt = pdef['interface']
        else:
            itxt = idef['name']
        if len(itxt) > 10:
            itxt = itxt[:7] + "..."
        frag = paper.tspan(itxt, dy=[pr + port_font_size])
        label = paper.text("", style=istyle, fill='#000000')
        label.add(frag)
        link.add(label)

    nb = len(node['outputs'])
    py = nh / 2
    for i, pdef in enumerate(node['outputs']):
        px = i * pspace - pspace * (nb - 1) / 2
        pg = g.add(paper.g())
        pg.translate(px, py)
        idef = store.get(pdef['interface'], None)
        if idef is not None and 'url' in idef:
            link = pg.add(paper.a(href=idef['url'], target='_top'))
        else:
            link = pg

        port = paper.circle((0, 0), pr, stroke='#000000', stroke_width=1)
        port.fill("url(#out_port)")
        link.add(port)
        # port name
        frag = paper.tspan(pdef['name'], dy=[2 * pr + port_font_size // 2])
        label = paper.text("", style=onstyle, fill='#000000')
        label.rotate(-45)
        label.add(frag)
        pg.add(label)
        # port interface
        if idef is None:
            itxt = pdef['interface']
        else:
            itxt = idef['name']
        if len(itxt) > 10:
            itxt = itxt[:7] + "..."
        frag = paper.tspan(itxt, dy=[- pr - 2])
        label = paper.text("", style=istyle, fill='#000000')
        label.add(frag)
        link.add(label)

    # reformat whole drawing to fit screen
    xmin = - nw / 2 - draw_padding / 10.
    xmax = + nw / 2 + draw_padding / 10.
    if len(node['inputs']) == 0:
        inames_extend = 0
    else:
        inames = [(len(pdef['name']), pdef['name']) for pdef in node['inputs']]
        inames_extend = (string_size(sorted(inames)[-1][1], port_font_size) +
                         port_font_size) * 0.7
    ymin = - nh / 2 - pr - inames_extend - draw_padding / 10.
    if len(node['outputs']) == 0:
        onames_extend = 0
    else:
        onames = [(len(pdef['name']), pdef['name']) for pdef in node['outputs']]
        onames_extend = (string_size(sorted(onames)[-1][1], port_font_size) +
                         port_font_size) * 0.7 + 2
    ymax = + nh / 2 + pr + onames_extend + draw_padding / 10.

    w = float(size[0])
    h = float(size[1])
    ratio = max((xmax - xmin) / w, (ymax - ymin) / h)
    xsize = int(ratio * w)
    ysize = int(ratio * h)

    paper.viewbox(-xsize / 2, -ysize / 2, xsize, ysize)

    return paper.tostring(), (-xsize / 2, -ysize / 2, xsize, ysize)
