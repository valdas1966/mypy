from f_search.ds.state import StateBase
from typing import TypeVar, Generic

State = TypeVar('State', bound=StateBase)


class HasDataState(Generic[State]):
    """
    ========================================================================
     Mixin for Data-Objects that can return State's stored Data.
    ========================================================================
    """

    def data_state(self, state: State) -> dict[str, any]:
        """
        ====================================================================
         Return a dict of State's stored Data (as key=value pairs).
        ====================================================================
        """
        return {'key': str(state.key)}
