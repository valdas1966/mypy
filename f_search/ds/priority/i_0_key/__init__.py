from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.ds.priority.i_0_key.main import PriorityKey

ULazy.install(globals(), {'PriorityKey': 'f_search.ds.priority.i_0_key.main:PriorityKey'})
