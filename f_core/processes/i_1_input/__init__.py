from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_core.processes.i_1_input.main import ProcessInput

ULazy.install(globals(), {'ProcessInput': 'f_core.processes.i_1_input.main:ProcessInput'})
