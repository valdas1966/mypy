from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_1_cell.main import StateCell
from f_ds.grids.cell.i_1_map import CellMap
from f_ds.grids.grid.map import GridMap


class ProblemGrid(ProblemSPP[StateCell]):
    """
    ============================================================================
     Shortest-Path-Problem on a 2D Grid.

     Pickles light: grid and derived StateCell cache are dropped on
     `__getstate__`. Rehydrate via `attach(grid, states=None)`. Use the
     `Store` helper for bulk save/load with grids in a separate file and
     a per-grid shared StateCell cache.
    ============================================================================
    """

    # Static Classes (wired in __init__.py)
    Factory: type = None
    Store: type = None
    Runner: type = None

    def __init__(self,
                 grid: GridMap,
                 start: CellMap,
                 goal: CellMap,
                 name: str = 'ProblemGrid') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # Stable identity (survives detach / pickle)
        self._grid_name: str = grid.name
        self._start_rc: tuple[int, int] = (start.row, start.col)
        self._goal_rc: tuple[int, int] = (goal.row, goal.col)
        # Heavy, derived attrs — populated by attach()
        self._grid: GridMap | None = None
        self._states: dict[CellMap, StateCell] | None = None
        ProblemSPP.__init__(self, starts=[], goals=[], name=name)
        self.attach(grid=grid)

    @property
    def grid(self) -> GridMap:
        """
        ========================================================================
         Return the Grid (raises if detached).
        ========================================================================
        """
        if self._grid is None:
            raise RuntimeError(
                f'{self.name!r}: grid not attached — '
                f'call attach(grid) first.')
        return self._grid

    @property
    def grid_name(self) -> str:
        """
        ========================================================================
         Return the Grid Name (stable — survives detach / pickle).
        ========================================================================
        """
        return self._grid_name

    @property
    def start_rc(self) -> tuple[int, int]:
        """
        ========================================================================
         Return the Start (row, col) (stable — survives detach / pickle).
        ========================================================================
        """
        return self._start_rc

    @property
    def goal_rc(self) -> tuple[int, int]:
        """
        ========================================================================
         Return the Goal (row, col) (stable — survives detach / pickle).
        ========================================================================
        """
        return self._goal_rc

    @property
    def is_attached(self) -> bool:
        """
        ========================================================================
         Return True when a Grid is attached and the Problem is usable.
        ========================================================================
        """
        return self._grid is not None

    def attach(self,
               grid: GridMap,
               states: dict[CellMap, StateCell] = None) -> None:
        """
        ========================================================================
         Rehydrate with a Grid and (optionally) a shared State cache.

         When `states` is None, a fresh cache is built (one StateCell per
         valid cell). Pass a shared cache dict to dedupe StateCell
         objects across multiple Problems sharing the same Grid.
        ========================================================================
        """
        # Sanity: grid identity must match
        if grid.name != self._grid_name:
            raise ValueError(
                f'Grid name mismatch: expected {self._grid_name!r}, '
                f'got {grid.name!r}.')
        self._grid = grid
        if states is None:
            states = {c: StateCell(key=c) for c in grid}
        self._states = states
        # Restore starts / goals from coords via the attached grid
        rs, cs = self._start_rc
        rg, cg = self._goal_rc
        self._starts = [self._states[grid[rs][cs]]]
        self._goals = [self._states[grid[rg][cg]]]

    def detach(self) -> None:
        """
        ========================================================================
         Drop the Grid and derived caches for light persistence.
        ========================================================================
        """
        self._grid = None
        self._states = None
        self._starts = []
        self._goals = []

    def successors(self,
                   state: StateCell) -> list[StateCell]:
        """
        ========================================================================
         Return the valid Grid Neighbors of the given State.
        ========================================================================
        """
        return [self._states[n]
                for n in self.grid.neighbors(state.key)]

    @property
    def key(self) -> tuple:
        """
        ========================================================================
         Return the Problem's Key for Equality (stable across attach /
         detach / pickle — based on grid name + start/goal coords).
        ========================================================================
        """
        return (self._grid_name, self._start_rc, self._goal_rc)

    def __hash__(self) -> int:
        """
        ========================================================================
         Return the Hash of the Problem.
        ========================================================================
        """
        return hash(self.key)

    def __getstate__(self) -> dict:
        """
        ========================================================================
         Return a light pickle state — drops grid and StateCell cache.
        ========================================================================
        """
        state = self.__dict__.copy()
        state['_grid'] = None
        state['_states'] = None
        state['_starts'] = []
        state['_goals'] = []
        return state

    def __setstate__(self, state: dict) -> None:
        """
        ========================================================================
         Restore from a light pickle state — Problem is detached until
         `attach(grid)` is called.
        ========================================================================
        """
        self.__dict__.update(state)
