from f_core.imports import ULazy

ULazy.install(globals(), {
    'GridBase': 'f_ds.grids.grid:GridBase',
    'GridMap': 'f_ds.grids.grid:GridMap',
    'CellMap': 'f_ds.grids.cell:CellMap',
    'Cluster': 'f_ds.grids.cluster:Cluster',
    'ClusterDiamond': 'f_ds.grids.cluster:ClusterDiamond',
    'PairCluster': 'f_ds.grids.cluster:PairCluster',
})
