from f_search.ds.data.i_0_base.main import DataSearch
from f_search.ds import StateBase as State
from f_search.ds import Path


class DataSPP(DataSearch):
    """
    ============================================================================
     Data for One-to-One Shortest-Path-Problem.
    ============================================================================
    """
    
    def path_to_best(self) -> Path:
        """
        ========================================================================
         Reconstruct the Path from Start to Best State.
        ========================================================================
        """
        states: list[State] = list()
        state = self.best
        while state:
            states.append(state)
            state = self.parent[state]
        states = states[::-1]
        return Path(states=states)
