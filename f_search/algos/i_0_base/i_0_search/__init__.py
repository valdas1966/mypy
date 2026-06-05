from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_0_base.i_0_search.main import AlgoSearch

ULazy.install(globals(), {'AlgoSearch': 'f_search.algos.i_0_base.i_0_search.main:AlgoSearch'})
