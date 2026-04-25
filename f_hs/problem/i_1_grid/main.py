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
                 start: CellMap | None = None,
                 goal: CellMap | None = None,
                 starts: list[CellMap] | None = None,
                 goals: list[CellMap] | None = None,
                 name: str = 'ProblemGrid') -> None:
        """
        ========================================================================
         Init private Attributes.

         Accepts either single (`start`, `goal`) or multi
         (`starts`, `goals`) endpoint forms; the two are
         mutually exclusive per side. Multi-form unlocks
         OMSPP / MOSPP / MMSPP problem instances on grids.
        ========================================================================
        """
        # Resolve start/starts: exactly one form per side.
        if (start is None) == (starts is None):
            raise ValueError(
                "exactly one of `start` or `starts` is required")
        if (goal is None) == (goals is None):
            raise ValueError(
                "exactly one of `goal` or `goals` is required")
        if start is not None:
            starts = [start]
        if goal is not None:
            goals = [goal]
        # Stable identity (survives detach / pickle)
        self._grid_name: str = grid.name
        self._starts_rc: list[tuple[int, int]] = [
            (c.row, c.col) for c in starts]
        self._goals_rc: list[tuple[int, int]] = [
            (c.row, c.col) for c in goals]
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
         Return the first Start (row, col) — convenience for single-start
         problems. Stable across detach / pickle.
        ========================================================================
        """
        return self._starts_rc[0]

    @property
    def goal_rc(self) -> tuple[int, int]:
        """
        ========================================================================
         Return the first Goal (row, col) — convenience for single-goal
         problems. Stable across detach / pickle.
        ========================================================================
        """
        return self._goals_rc[0]

    @property
    def starts_rc(self) -> list[tuple[int, int]]:
        """
        ========================================================================
         Return the list of Start (row, col) tuples (stable — survives
         detach / pickle).
        ========================================================================
        """
        return list(self._starts_rc)

    @property
    def goals_rc(self) -> list[tuple[int, int]]:
        """
        ========================================================================
         Return the list of Goal (row, col) tuples (stable — survives
         detach / pickle).
        ========================================================================
        """
        return list(self._goals_rc)

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
        self._starts = [self._states[grid[r][c]]
                        for r, c in self._starts_rc]
        self._goals = [self._states[grid[r][c]]
                       for r, c in self._goals_rc]

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
        return (self._grid_name,
                tuple(self._starts_rc),
                tuple(self._goals_rc))

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

    def __repr__(self) -> str:
        """
        ========================================================================
         Return a debugger-friendly representation:
         '<ProblemGrid: grid=X, #starts=k1, #goals=k2,
         avg_dist_starts_to_goals=..., avg_dist_between_goals=...>'.
         Distances are Manhattan over (row, col); computed from the
         stable rc lists, so __repr__ works detached and after pickle.
        ========================================================================
        """
        starts = self._starts_rc
        goals = self._goals_rc
        # avg Manhattan dist over all (start, goal) pairs.
        if starts and goals:
            avg_sg = (sum(abs(sr - gr) + abs(sc - gc)
                          for sr, sc in starts
                          for gr, gc in goals)
                      / (len(starts) * len(goals)))
        else:
            avg_sg = 0.0
        # avg Manhattan dist over all unordered goal-goal pairs.
        if len(goals) >= 2:
            n_pairs = len(goals) * (len(goals) - 1) // 2
            total = 0
            for i in range(len(goals)):
                gri, gci = goals[i]
                for j in range(i + 1, len(goals)):
                    grj, gcj = goals[j]
                    total += abs(gri - grj) + abs(gci - gcj)
            avg_gg = total / n_pairs
        else:
            avg_gg = 0.0
        return (f'<{type(self).__name__}: '
                f'grid={self._grid_name}, '
                f'#starts={len(starts)}, '
                f'#goals={len(goals)}, '
                f'avg_dist_starts_to_goals={avg_sg:.2f}, '
                f'avg_dist_between_goals={avg_gg:.2f}>')
