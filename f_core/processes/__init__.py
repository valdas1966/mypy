from f_core.imports import ULazy

ULazy.install(globals(), {
    'ProcessIO': 'f_core.processes.i_2_io:ProcessIO',
    'ProcessParallel': 'f_core.processes.i_3_parallel:ProcessParallel',
})
