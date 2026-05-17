from f_core.imports import ULazy

ULazy.install(globals(), {
    'HasStart': 'f_search.problems.mixins.has_start.main:HasStart',
    'State': 'f_search.problems.mixins.has_start.main:State',
})
