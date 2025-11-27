from f_search.ds.data.i_0_base.main import DataSearch
from f_search.ds import StateBase as State
from f_search.ds import Path


class DataSPP(DataSearch):
    """
    ============================================================================
     Data for One-to-One Shortest-Path-Problem.
    ============================================================================
    """
    
    def path_to(self, state: State) -> Path:
        """
        ========================================================================
         Reconstruct the Path from Start to Best State.
        ========================================================================
        """
        states: list[State] = list()
        cur = state
        while cur:
            states.append(cur)
            cur = self.parent[cur]
        states = states[::-1]
        path = Path(states=states)
        print(self.best, path)
        return Path(states=states)
