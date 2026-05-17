from f_core.imports import ULazy

ULazy.install(globals(), {
    'ProblemSearch': 'f_search.problems.i_0_base:ProblemSearch',
    'ProblemSPP': 'f_search.problems.i_1_spp:ProblemSPP',
    'ProblemOMSPP': 'f_search.problems.i_2_omspp:ProblemOMSPP',
    'ProblemMMSPP': 'f_search.problems.i_3_mmspp:ProblemMMSPP',
    'ProblemNeighborhood': 'f_search.problems.i_1_neighborhood:ProblemNeighborhood',
})
