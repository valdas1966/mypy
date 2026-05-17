from f_core.imports import ULazy

ULazy.install(globals(), {
    'GridBase': 'f_ds.grids.grid.base:GridBase',
    'GridMap': 'f_ds.grids.grid.map:GridMap',
})
