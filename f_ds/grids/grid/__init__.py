from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_ds.grids.grid.base import GridBase
    from f_ds.grids.grid.map import GridMap

ULazy.install(globals(), {
    'GridBase': 'f_ds.grids.grid.base:GridBase',
    'GridMap': 'f_ds.grids.grid.map:GridMap',
})
