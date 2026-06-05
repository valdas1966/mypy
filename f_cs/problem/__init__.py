from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_cs.problem.main import ProblemAlgo

ULazy.install(globals(), {'ProblemAlgo': 'f_cs.problem.main:ProblemAlgo'})
