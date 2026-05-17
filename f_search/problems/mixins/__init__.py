from f_core.imports import ULazy

ULazy.install(globals(), {
    'HasStart': 'f_search.problems.mixins.has_start:HasStart',
    'HasStarts': 'f_search.problems.mixins.has_starts:HasStarts',
    'HasGoal': 'f_search.problems.mixins.has_goal:HasGoal',
    'HasGoals': 'f_search.problems.mixins.has_goals:HasGoals',
})
