from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .i_0_base import ConnectivityBase
    from .i_1_04 import Connectivity_4
    from .i_1_08 import Connectivity_8

ULazy.install(globals(), {
    'ConnectivityBase': '.i_0_base:ConnectivityBase',
    'Connectivity_4': '.i_1_04:Connectivity_4',
    'Connectivity_8': '.i_1_08:Connectivity_8',
})
