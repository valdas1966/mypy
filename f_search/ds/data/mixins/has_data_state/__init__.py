from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.ds.data.mixins.has_data_state.main import HasDataState

ULazy.install(globals(), {'HasDataState': 'f_search.ds.data.mixins.has_data_state.main:HasDataState'})
