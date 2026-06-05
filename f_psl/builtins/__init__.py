from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_psl.builtins.list import UList

ULazy.install(globals(), {'UList': 'f_psl.builtins.list:UList'})
