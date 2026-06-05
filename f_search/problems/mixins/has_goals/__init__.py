from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.problems.mixins.has_goals.main import HasGoals

ULazy.install(globals(), {'HasGoals': 'f_search.problems.mixins.has_goals.main:HasGoals'})
