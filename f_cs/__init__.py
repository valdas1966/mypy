from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_cs.algo import Algo
    from f_cs.problem import ProblemAlgo
    from f_cs.solution import SolutionAlgo

ULazy.install(globals(), {
    'Algo': 'f_cs.algo:Algo',
    'ProblemAlgo': 'f_cs.problem:ProblemAlgo',
    'SolutionAlgo': 'f_cs.solution:SolutionAlgo',
})
