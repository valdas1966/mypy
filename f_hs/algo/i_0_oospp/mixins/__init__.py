from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.algo.i_0_oospp.mixins.bpmx import BPMXMixin

ULazy.install(globals(), {'BPMXMixin': 'f_hs.algo.i_0_oospp.mixins.bpmx:BPMXMixin'})
