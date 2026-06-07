from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_ds.geometry.bounds import Bounds
    from f_ds.geometry.point import Point

ULazy.install(globals(), {
    'Bounds': 'f_ds.geometry.bounds:Bounds',
    'Point': 'f_ds.geometry.point:Point',
})
