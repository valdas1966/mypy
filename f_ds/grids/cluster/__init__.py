from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .i_0_base import ClusterGrid
    from .i_1_diamond import ClusterDiamond

ULazy.install(globals(), {
    'ClusterGrid': '.i_0_base:ClusterGrid',
    'ClusterDiamond': '.i_1_diamond:ClusterDiamond',
})
