from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_color.rgb import RGB

ULazy.install(globals(), {'RGB': 'f_color.rgb:RGB'})
