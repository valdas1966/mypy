from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.ds.data.mixins import HasDataState
    from f_search.ds.data.i_0_best_first import DataBestFirst
    from f_search.ds.data.i_1_heuristics import DataHeuristics
    from f_search.ds.data.i_2_heuristics_vector import DataHeuristicsVector
    from f_search.ds.data.cached import DataCached

ULazy.install(globals(), {
    'HasDataState': 'f_search.ds.data.mixins:HasDataState',
    'DataBestFirst': 'f_search.ds.data.i_0_best_first:DataBestFirst',
    'DataHeuristics': 'f_search.ds.data.i_1_heuristics:DataHeuristics',
    'DataHeuristicsVector': 'f_search.ds.data.i_2_heuristics_vector:DataHeuristicsVector',
    'DataCached': 'f_search.ds.data.cached:DataCached',
})
