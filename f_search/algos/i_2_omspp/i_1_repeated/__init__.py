from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_2_omspp.i_1_repeated.astar import AStarRepeated
    from f_search.algos.i_2_omspp.i_1_repeated.astar_backward import AStarRepeatedBackward

ULazy.install(globals(), {
    'AStarRepeated': 'f_search.algos.i_2_omspp.i_1_repeated.astar:AStarRepeated',
    'AStarRepeatedBackward': 'f_search.algos.i_2_omspp.i_1_repeated.astar_backward:AStarRepeatedBackward',
})
