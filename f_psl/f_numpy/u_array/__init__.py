from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_psl.f_numpy.u_array.main import UArray

ULazy.install(globals(), {'UArray': 'f_psl.f_numpy.u_array.main:UArray'})
