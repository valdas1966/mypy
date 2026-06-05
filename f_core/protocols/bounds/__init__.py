from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.protocols.bounds.main import SupportsBounds

ULazy.install(globals(), {'SupportsBounds': 'f_core.protocols.bounds.main:SupportsBounds'})
