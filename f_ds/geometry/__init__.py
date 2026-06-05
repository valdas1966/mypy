from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_ds.geometry.bounds import Bounds

ULazy.install(globals(), {'Bounds': 'f_ds.geometry.bounds:Bounds'})
