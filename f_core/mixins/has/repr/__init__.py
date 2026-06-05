from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.mixins.has.repr.main import HasRepr

ULazy.install(globals(), {'HasRepr': 'f_core.mixins.has.repr.main:HasRepr'})
