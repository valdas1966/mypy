from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:                        # analyzers only — never runs
    from f_ds.clusters.i_0_base import ClusterBase
    from f_ds.clusters.i_1_list import ClusterList

ULazy.install(globals(), {
    'ClusterBase': 'f_ds.clusters.i_0_base:ClusterBase',
    'ClusterList': 'f_ds.clusters.i_1_list:ClusterList',
})
