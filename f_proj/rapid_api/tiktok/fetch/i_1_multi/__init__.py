from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .main import FetchMulti

ULazy.install(globals(), {'FetchMulti': '.main:FetchMulti'})
