from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .u_file_map import UFileMap

ULazy.install(globals(), {'UFileMap': '.u_file_map:UFileMap'})
