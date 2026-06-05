from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_psl.file import u_txt

ULazy.install(globals(), {'u_txt': 'f_psl.file.u_txt'})
