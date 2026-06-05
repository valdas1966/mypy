from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.solutions.i_0_base import SolutionSearch
    from f_search.solutions.i_1_spp import SolutionSPP
    from f_search.solutions.i_2_omspp import SolutionOMSPP
    from f_search.solutions.i_1_neighborhood import SolutionNeighborhood

ULazy.install(globals(), {
    'SolutionSearch': 'f_search.solutions.i_0_base:SolutionSearch',
    'SolutionSPP': 'f_search.solutions.i_1_spp:SolutionSPP',
    'SolutionOMSPP': 'f_search.solutions.i_2_omspp:SolutionOMSPP',
    'SolutionNeighborhood': 'f_search.solutions.i_1_neighborhood:SolutionNeighborhood',
})
