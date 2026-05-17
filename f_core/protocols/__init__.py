from f_core.imports import ULazy

ULazy.install(globals(), {
    'SupportsEquality': 'f_core.protocols.equality:SupportsEquality',
    'SupportsComparison': 'f_core.protocols.comparison:SupportsComparison',
    'SupportsBounds': 'f_core.protocols.bounds:SupportsBounds',
})
