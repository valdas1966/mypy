from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .i_0_base import Cluster
    from .i_1_diamond import ClusterDiamond
    from .pair import PairCluster

ULazy.install(globals(), {
    'Cluster': '.i_0_base:Cluster',
    'ClusterDiamond': '.i_1_diamond:ClusterDiamond',
    'PairCluster': '.pair:PairCluster',
})
