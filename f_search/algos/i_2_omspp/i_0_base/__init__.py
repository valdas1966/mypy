from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_2_omspp.i_0_base.main import AlgoOMSPP

ULazy.install(globals(), {'AlgoOMSPP': 'f_search.algos.i_2_omspp.i_0_base.main:AlgoOMSPP'})
