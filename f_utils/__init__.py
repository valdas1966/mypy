from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_utils.iter import u_iter

ULazy.install(globals(), {'u_iter': 'f_utils.iter.u_iter'})
