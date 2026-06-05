from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.algo.i_0_oospp.i_0_base.main import AlgoSPP
    from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP

ULazy.install(globals(), {
    'AlgoSPP': 'f_hs.algo.i_0_oospp.i_0_base.main:AlgoSPP',
    'SearchStateSPP': 'f_hs.algo.i_0_oospp.i_0_base._search_state:SearchStateSPP',
})
