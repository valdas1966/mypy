from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.problems.mixins.has_start.main import HasStart
    from f_search.problems.mixins.has_start.main import State

ULazy.install(globals(), {
    'HasStart': 'f_search.problems.mixins.has_start.main:HasStart',
    'State': 'f_search.problems.mixins.has_start.main:State',
})
