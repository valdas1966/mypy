from f_core.processes.process import Process
from f_ds.grids import GridMap as Grid
from f_utils import u_pickle


class LoadGrids(Process[str, dict[str, dict[str, Grid]]]):
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """

    def _run(self) -> dict[str, dict[str, Grid]]:
        """
        ========================================================================
         Return the grids from the pickle file.
        ========================================================================
        """
        return u_pickle.load(path='g:\\paper\\grids.pkl')