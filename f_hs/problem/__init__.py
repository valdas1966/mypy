from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.problem.i_0_base import ProblemSPP
    from f_hs.problem.i_1_grid import ProblemGrid

ULazy.install(globals(), {
    'ProblemSPP': 'f_hs.problem.i_0_base:ProblemSPP',
    'ProblemGrid': 'f_hs.problem.i_1_grid:ProblemGrid',
})
