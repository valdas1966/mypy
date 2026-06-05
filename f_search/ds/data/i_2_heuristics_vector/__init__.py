from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.ds.data.i_2_heuristics_vector.main import DataHeuristicsVector

ULazy.install(globals(), {'DataHeuristicsVector': 'f_search.ds.data.i_2_heuristics_vector.main:DataHeuristicsVector'})
