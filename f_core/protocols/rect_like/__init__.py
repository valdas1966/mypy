from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.protocols.rect_like.main import RectLike

ULazy.install(globals(), {'RectLike': 'f_core.protocols.rect_like.main:RectLike'})
