from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_ds.geometry.bounds import Bounds
    from f_ds.geometry.pointxy import PointXY
    from f_ds.geometry.point2d import Point2D
    from f_ds.geometry.side import Side

ULazy.install(globals(), {
    'Bounds': 'f_ds.geometry.bounds:Bounds',
    'PointXY': 'f_ds.geometry.pointxy:PointXY',
    'Point2D': 'f_ds.geometry.point2d:Point2D',
    'Side': 'f_ds.geometry.side:Side',
})
