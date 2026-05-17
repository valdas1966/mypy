from f_core.imports import ULazy

ULazy.install(globals(), {
    'AStarRepeated': 'f_search.algos.i_2_omspp.i_1_repeated.astar:AStarRepeated',
    'AStarRepeatedBackward': 'f_search.algos.i_2_omspp.i_1_repeated.astar_backward:AStarRepeatedBackward',
})
