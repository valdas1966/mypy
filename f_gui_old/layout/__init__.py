from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_gui_old.layout.bounds.main import Bounds

ULazy.install(globals(), {'Bounds': 'f_gui_old.layout.bounds.main:Bounds'})
