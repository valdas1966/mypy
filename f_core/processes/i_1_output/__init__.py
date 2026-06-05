from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.processes.i_1_output.main import ProcessOutput

ULazy.install(globals(), {'ProcessOutput': 'f_core.processes.i_1_output.main:ProcessOutput'})
