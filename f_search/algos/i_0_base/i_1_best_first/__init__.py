from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_0_base.i_1_best_first.main import AlgoBestFirst

ULazy.install(globals(), {'AlgoBestFirst': 'f_search.algos.i_0_base.i_1_best_first.main:AlgoBestFirst'})
