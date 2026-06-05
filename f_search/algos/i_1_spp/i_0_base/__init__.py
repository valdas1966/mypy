from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_1_spp.i_0_base.main import AlgoSPP

ULazy.install(globals(), {'AlgoSPP': 'f_search.algos.i_1_spp.i_0_base.main:AlgoSPP'})
