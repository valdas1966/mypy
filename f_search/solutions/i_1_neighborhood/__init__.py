from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.solutions.i_1_neighborhood.main import SolutionNeighborhood

ULazy.install(globals(), {'SolutionNeighborhood': 'f_search.solutions.i_1_neighborhood.main:SolutionNeighborhood'})
