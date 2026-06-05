from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.protocols.comparison.main import SupportsComparison

ULazy.install(globals(), {'SupportsComparison': 'f_core.protocols.comparison.main:SupportsComparison'})
