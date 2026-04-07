from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_1_cell.main import StateCell
from f_ds.grids.cell.i_1_map import CellMap
from f_ds.grids.grid.map import GridMap


class ProblemGrid(ProblemSPP[StateCell]):
    """
    ========================================================================
     Shortest-Path-Problem on a 2D Grid.
    ========================================================================
    """

    def __init__(self,
                 grid: GridMap,
                 start: CellMap,
                 goal: CellMap,
                 name: str = 'ProblemGrid') -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self._grid = grid
        # Cache: one StateCell per valid cell
        self._states: dict[CellMap, StateCell] = {
            cell: StateCell(key=cell) for cell in grid
        }
        ProblemSPP.__init__(
            self,
            starts=[self._states[start]],
            goals=[self._states[goal]],
            name=name,
        )

    @property
    def grid(self) -> GridMap:
        """
        ====================================================================
         Return the Grid.
        ====================================================================
        """
        return self._grid

    def successors(self,
                   state: StateCell) -> list[StateCell]:
        """
        ====================================================================
         Return the valid Grid Neighbors of the given State.
        ====================================================================
        """
        return [self._states[n]
                for n in self._grid.neighbors(state.key)]
