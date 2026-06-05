from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.problems.mixins.has_goal.main import HasGoal

ULazy.install(globals(), {'HasGoal': 'f_search.problems.mixins.has_goal.main:HasGoal'})
