from f_core.imports import ULazy

ULazy.install(globals(), {
    'UPercentiles': 'f_math.percentiles.utils:UPercentiles',
    'Bin': 'f_math.percentiles.bin:Bin',
})
