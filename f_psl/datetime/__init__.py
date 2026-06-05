from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_psl.datetime.main import UDateTime

ULazy.install(globals(), {'UDateTime': 'f_psl.datetime.main:UDateTime'})
