from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .i_0_base import ConnectivityBase
    from .i_1_four import Connectivity4
    from .i_1_eight import Connectivity8

ULazy.install(globals(), {
    'ConnectivityBase': '.i_0_base:ConnectivityBase',
    'Connectivity4': '.i_1_four:Connectivity4',
    'Connectivity8': '.i_1_eight:Connectivity8',
})
