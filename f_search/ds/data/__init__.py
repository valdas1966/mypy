from f_core.imports import ULazy

ULazy.install(globals(), {
    'HasDataState': 'f_search.ds.data.mixins:HasDataState',
    'DataBestFirst': 'f_search.ds.data.i_0_best_first:DataBestFirst',
    'DataHeuristics': 'f_search.ds.data.i_1_heuristics:DataHeuristics',
    'DataHeuristicsVector': 'f_search.ds.data.i_2_heuristics_vector:DataHeuristicsVector',
    'DataCached': 'f_search.ds.data.cached:DataCached',
})
