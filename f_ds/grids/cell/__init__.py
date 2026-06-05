from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .i_0_base import CellBase
    from .i_1_map import CellMap

ULazy.install(globals(), {
    'CellBase': '.i_0_base:CellBase',
    'CellMap': '.i_1_map:CellMap',
})
