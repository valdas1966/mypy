from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .i_0_grid import ClusterGrid
    from .i_1_diamond import ClusterDiamond
    from .pair import PairCluster

ULazy.install(globals(), {
    'ClusterGrid': '.i_0_grid:ClusterGrid',
    'ClusterDiamond': '.i_1_diamond:ClusterDiamond',
    'PairCluster': '.pair:PairCluster',
})
