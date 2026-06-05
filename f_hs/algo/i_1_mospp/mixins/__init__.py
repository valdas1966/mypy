from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.algo.i_1_mospp.mixins.extendable import ExtendableMOSPP
    from f_hs.algo.i_1_mospp.mixins.extendable import is_extendable

ULazy.install(globals(), {
    'ExtendableMOSPP': 'f_hs.algo.i_1_mospp.mixins.extendable:ExtendableMOSPP',
    'is_extendable': 'f_hs.algo.i_1_mospp.mixins.extendable:is_extendable',
})
