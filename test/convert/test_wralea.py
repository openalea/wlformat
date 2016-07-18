try:
    from openalea import core
    run_test = True
except ImportError:
    core = None
    run_test = False

if run_test:
    from openalea.core import Factory as NF
    from openalea.core import CompositeNodeFactory as CNF
    from openalea.wlformat.convert import wralea


    def test_convert_node():
        nf = NF(name="color",
                authors="moi",
                description="edit color",
                category="datatype, image",
                nodemodule="openalea.color.py_color",
                nodeclass="ColorNode",
                inputs=(dict(name="RGB",
                             interface="triplet",
                             value=(0, 0, 0)),),
                outputs=(dict(name="RGB", interface="rgb"),),
                )

        store = {}
        wralea.register_interface(store, "triplet")
        wralea.register_interface(store, "rgb")
        ndef = wralea.convert_node(nf, store, "pkg")

        assert len(store) == 2
        assert 'color' in ndef['name']
        assert ndef['description'] == nf.description
        assert len(ndef['inputs']) == 1
        assert len(ndef['outputs']) == 1


    def test_convert_node_reuse_interfaces_definitions():
        nf = NF(name="color",
                authors="moi",
                description="edit color",
                category="datatype, image",
                nodemodule="openalea.color.py_color",
                nodeclass="ColorNode",
                inputs=(dict(name="RGB",
                             interface="triplet",
                             value=(0, 0, 0)),),
                outputs=(dict(name="RGB", interface="rgb"),),
                )

        store = {}
        wralea.register_interface(store, "triplet")
        wralea.register_interface(store, "rgb")
        ndef = wralea.convert_node(nf, store, "pkg")
        assert len(store) == 2

        ndef2 = wralea.convert_node(nf, store, "pkg")

        assert len(store) == 2
        assert ndef2['inputs'][0]['interface'] == ndef['inputs'][0]['interface']
        assert ndef2['outputs'][0]['interface'] == ndef['outputs'][0]['interface']


    def test_convert_node_handle_none_instead_of_empty_lists():
        nf = NF(name="color",
                authors="moi",
                description="edit color",
                category="datatype, image",
                nodemodule="openalea.color.py_color",
                nodeclass="ColorNode")

        store = {}
        ndef = wralea.convert_node(nf, store, "pkg")
        assert len(store) == 0
        assert len(ndef['inputs']) == 0
        assert len(ndef['outputs']) == 0


    def test_convert_workflow():
        cnf = CNF(name='dummy',
                  authors="moi",
                  description='Some description',
                  category='doofus',
                  doc='Some Documentation',
                  inputs=[],
                  outputs=[],
                  elt_factory={
                      2: ('openalea.numpy.creation', 'array'),
                      3: ('openalea.data structure.list', 'list'),
                      4: ('openalea.data structure.list', 'list')},
                  elt_connections={4297110208: (2, 0, 3, 0),
                                   4297110232: (2, 1, 3, 1)},
                  elt_data={2: {'block': True,
                                'caption': 'array',
                                'delay': 1,
                                'factory': 'fac array',
                                'hide': True,
                                'id': 2,
                                'lazy': False,
                                'port_hide_changed': set(),
                                'priority': 1,
                                'use_user_color': True,
                                'user_application': 'toto',
                                'user_color': (0, 0, 0)},
                            3: {'block': False,
                                'caption': 'list',
                                'delay': 0,
                                'factory': 'fac list',
                                'hide': True,
                                'id': 3,
                                'lazy': True,
                                'port_hide_changed': set(),
                                'posx': -607.1703903388244,
                                'posy': -85.555388524075241,
                                'priority': 0,
                                'use_user_color': False,
                                'user_application': None,
                                'user_color': None},
                            4: {'block': False,
                                'caption': 'list',
                                'delay': 0,
                                'factory': 'fac list',
                                'hide': True,
                                'id': 3,
                                'lazy': True,
                                'port_hide_changed': set(),
                                'posx': -607.1703903388244,
                                'posy': -85.555388524075241,
                                'priority': 0}
                            },
                  elt_value={2: [(1, "'float64'"), (2, 'True'),
                                 (3, "'C'"), (4, 'False'),
                                 (5, '0')],
                             3: [(0,
                                  '[(1.5, 2, 3), (4, 5, 6)]')]},
                  elt_ad_hoc={2: {'position': [-569.97322483814833,
                                               -21.496113928672312],
                                  'userColor': None,
                                  'useUserColor': False},
                              3: {'position': [
                                  -607.1703903388244,
                                  -85.555388524075241],
                                  'userColor': None,
                                  'useUserColor': False},
                              4: {'position': [
                                  -607.1703903388244,
                                  -85.555388524075241],
                                  'userColor': (0, 0, 0),
                                  'useUserColor': True}
                              },
                  lazy=True,
                  eval_algo='LambdaEvaluation',
                  )

        store = {}
        idef = wralea.register_interface(store, "any")
        ndef = wralea.register_node(store, ('openalea.numpy.creation', 'array'))
        ndef['outputs'] = [dict(name="out0",
                                interface=idef['id'],
                                default="",
                                description=""),
                           dict(name="out1",
                                interface=idef['id'],
                                default="",
                                description="")]
        ndef = wralea.register_node(store,
                                    ('openalea.data structure.list', 'list'))
        ndef['inputs'] = [dict(name="in0",
                               interface=idef['id'],
                               default="",
                               description=""),
                          dict(name="in1",
                               interface=idef['id'],
                               default="",
                               description="")]
        wdef = wralea.convert_workflow(cnf, store)

        assert len(store) == 3
        assert wdef['description'] == cnf.description
        assert len(wdef['nodes']) == 3
        assert len(wdef['links']) == 2


    def test_convert_workflow_reuse_node_definitions():
        cnf = CNF(name='dummy',
                  authors="moi",
                  description='Some description',
                  category='doofus',
                  doc='Some Documentation',
                  inputs=[],
                  outputs=[],
                  elt_factory={
                      2: ('openalea.numpy.creation', 'array'),
                      3: ('openalea.data structure.list', 'list')},
                  elt_connections={4297110208: (2, 0, 3, 0),
                                   4297110232: (2, 1, 3, 1)},
                  )

        store = {}
        idef = wralea.register_interface(store, "any")
        ndef = wralea.register_node(store, ('openalea.numpy.creation', 'array'))
        ndef['outputs'] = [dict(name="out0",
                                interface=idef['id'],
                                default="",
                                description=""),
                           dict(name="out1",
                                interface=idef['id'],
                                default="",
                                description="")]
        ndef = wralea.register_node(store,
                                    ('openalea.data structure.list', 'list'))
        ndef['inputs'] = [dict(name="in0",
                               interface=idef['id'],
                               default="",
                               description=""),
                          dict(name="in1",
                               interface=idef['id'],
                               default="",
                               description="")]
        wdef = wralea.convert_workflow(cnf, store)
        assert len(store) == 3

        wdef2 = wralea.convert_workflow(cnf, store)
        assert len(store) == 3

        assert wdef2['nodes'][0]['id'] == wdef['nodes'][0]['id']


    def test_convert_workflow_return_none_for_composite_nodes():
        cnf = CNF(name='dummy',
                  authors="moi",
                  description='Some description',
                  category='doofus',
                  doc='Some Documentation',
                  inputs=[],
                  outputs=[],
                  elt_factory={
                      2: ('openalea.numpy.creation', 'array'),
                      3: ('openalea.data structure.list', 'list')},
                  elt_connections={4297110208: ('__in__', 0, 3, 0),
                                   4297110232: (2, 1, '__out__', 1)},
                  )

        store = {}
        wdef = wralea.convert_workflow(cnf, store)
        assert wdef is None
