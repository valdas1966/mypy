from f_core.imports import ULazy

ULazy.install(globals(), {
    'SolutionSearch': 'f_search.solutions.i_0_base:SolutionSearch',
    'SolutionSPP': 'f_search.solutions.i_1_spp:SolutionSPP',
    'SolutionOMSPP': 'f_search.solutions.i_2_omspp:SolutionOMSPP',
    'SolutionNeighborhood': 'f_search.solutions.i_1_neighborhood:SolutionNeighborhood',
})
