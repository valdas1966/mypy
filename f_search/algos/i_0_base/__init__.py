from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_0_base.i_0_search import AlgoSearch
    from f_search.algos.i_0_base.i_1_best_first import AlgoBestFirst

ULazy.install(globals(), {
    'AlgoSearch': 'f_search.algos.i_0_base.i_0_search:AlgoSearch',
    'AlgoBestFirst': 'f_search.algos.i_0_base.i_1_best_first:AlgoBestFirst',
})
