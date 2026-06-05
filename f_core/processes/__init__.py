from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.processes.i_2_io import ProcessIO
    from f_core.processes.i_3_parallel import ProcessParallel

ULazy.install(globals(), {
    'ProcessIO': 'f_core.processes.i_2_io:ProcessIO',
    'ProcessParallel': 'f_core.processes.i_3_parallel:ProcessParallel',
})
