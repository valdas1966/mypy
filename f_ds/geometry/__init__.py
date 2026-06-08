from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_ds.geometry.bounds import Bounds
    from f_ds.geometry.point import Point
    from f_ds.geometry.side import Side

ULazy.install(globals(), {
    'Bounds': 'f_ds.geometry.bounds:Bounds',
    'Point': 'f_ds.geometry.point:Point',
    'Side': 'f_ds.geometry.side:Side',
})
