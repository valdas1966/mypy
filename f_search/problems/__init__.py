from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.problems.i_0_base import ProblemSearch
    from f_search.problems.i_1_spp import ProblemSPP
    from f_search.problems.i_2_omspp import ProblemOMSPP
    from f_search.problems.i_3_mmspp import ProblemMMSPP
    from f_search.problems.i_1_neighborhood import ProblemNeighborhood

ULazy.install(globals(), {
    'ProblemSearch': 'f_search.problems.i_0_base:ProblemSearch',
    'ProblemSPP': 'f_search.problems.i_1_spp:ProblemSPP',
    'ProblemOMSPP': 'f_search.problems.i_2_omspp:ProblemOMSPP',
    'ProblemMMSPP': 'f_search.problems.i_3_mmspp:ProblemMMSPP',
    'ProblemNeighborhood': 'f_search.problems.i_1_neighborhood:ProblemNeighborhood',
})
