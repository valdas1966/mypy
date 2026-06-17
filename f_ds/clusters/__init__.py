from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:                        # analyzers only — never runs
    from f_ds.clusters.i_0_base import Cluster

ULazy.install(globals(), {
    'Cluster': 'f_ds.clusters.i_0_base:Cluster',
})
