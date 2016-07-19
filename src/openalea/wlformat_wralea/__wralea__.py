"""node definition to interact with SEE platform
"""

from openalea.core import Factory
from openalea.core.interface import *

__name__ = "openalea.wlformat"
__alias__ = []
__version__ = '0.0.3'
__license__ = "Cecill-C"
__authors__ = 'Jerome Chopard'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Nodes to interact with provenance'
__url__ = ''

__all__ = []

dp = Factory(name="data_produced_by",
             description="",
             category="",
             nodemodule="openalea.wlformat.prov_exe",
             nodeclass="data_produced_by",
             inputs=(dict(name="prov", interface=None),
                     dict(name="node", interface=IInt),
                     dict(name="port", interface=IStr),),
             outputs=(dict(name="id", interface=IStr),
                      dict(name="val", interface=None),),
             )

__all__.append('dp')


du = Factory(name="data_used_by",
             description="",
             category="",
             nodemodule="openalea.wlformat.prov_exe",
             nodeclass="data_used_by",
             inputs=(dict(name="prov", interface=None),
                     dict(name="node", interface=IInt),
                     dict(name="port", interface=IStr),),
             outputs=(dict(name="id", interface=IStr),
                      dict(name="val", interface=None),),
             )

__all__.append('du')
