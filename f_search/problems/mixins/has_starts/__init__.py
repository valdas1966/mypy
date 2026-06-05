from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.problems.mixins.has_starts.main import HasStarts

ULazy.install(globals(), {'HasStarts': 'f_search.problems.mixins.has_starts.main:HasStarts'})
