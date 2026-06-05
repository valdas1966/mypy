from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_cs.solution.main import SolutionAlgo

ULazy.install(globals(), {'SolutionAlgo': 'f_cs.solution.main:SolutionAlgo'})
