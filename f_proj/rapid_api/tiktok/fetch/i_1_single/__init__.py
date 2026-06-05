from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .main import FetchSingle

ULazy.install(globals(), {'FetchSingle': '.main:FetchSingle'})
