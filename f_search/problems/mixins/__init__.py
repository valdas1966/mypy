from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.problems.mixins.has_start import HasStart
    from f_search.problems.mixins.has_starts import HasStarts
    from f_search.problems.mixins.has_goal import HasGoal
    from f_search.problems.mixins.has_goals import HasGoals

ULazy.install(globals(), {
    'HasStart': 'f_search.problems.mixins.has_start:HasStart',
    'HasStarts': 'f_search.problems.mixins.has_starts:HasStarts',
    'HasGoal': 'f_search.problems.mixins.has_goal:HasGoal',
    'HasGoals': 'f_search.problems.mixins.has_goals:HasGoals',
})
