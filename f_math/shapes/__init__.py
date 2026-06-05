from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_math.shapes.rect import Rect

ULazy.install(globals(), {'Rect': 'f_math.shapes.rect:Rect'})
