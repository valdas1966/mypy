from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.algo.i_1_omspp.mixins.extendable import ExtendableOMSPP
    from f_hs.algo.i_1_omspp.mixins.extendable import is_extendable

ULazy.install(globals(), {
    'ExtendableOMSPP': 'f_hs.algo.i_1_omspp.mixins.extendable:ExtendableOMSPP',
    'is_extendable': 'f_hs.algo.i_1_omspp.mixins.extendable:is_extendable',
})
