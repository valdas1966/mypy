from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.mixins.sizable.main import Sizable

ULazy.install(globals(), {'Sizable': 'f_core.mixins.sizable.main:Sizable'})
