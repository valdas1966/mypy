from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_ds.grids.grid import GridBase
    from f_ds.grids.grid import GridMap
    from f_ds.grids.cell import CellMap
    from f_ds.grids.cluster import Cluster
    from f_ds.grids.cluster import ClusterDiamond
    from f_ds.grids.cluster import PairCluster

ULazy.install(globals(), {
    'GridBase': 'f_ds.grids.grid:GridBase',
    'GridMap': 'f_ds.grids.grid:GridMap',
    'CellMap': 'f_ds.grids.cell:CellMap',
    'Cluster': 'f_ds.grids.cluster:Cluster',
    'ClusterDiamond': 'f_ds.grids.cluster:ClusterDiamond',
    'PairCluster': 'f_ds.grids.cluster:PairCluster',
})
