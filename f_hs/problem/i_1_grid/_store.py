import pickle

from f_hs.problem.i_1_grid.main import ProblemGrid
from f_hs.state.i_1_cell.main import StateCell
from f_ds.grids.grid.map import GridMap


class Store:
    """
    ============================================================================
     Bulk save / load for ProblemGrid instances with grids stored in a
     separate pickle file.

     Save path: grids -> `path_grids`, problems (detached) -> `path_problems`.
     Load path: grids are loaded first; each Problem is rehydrated via
     `attach()` using a shared per-grid StateCell cache — so N Problems
     pointing at the same Grid share a single StateCell dict.
    ============================================================================
    """

    @staticmethod
    def save(problems: list[ProblemGrid],
             grids: dict[str, GridMap],
             path_problems: str,
             path_grids: str) -> None:
        """
        ========================================================================
         Save the grids and (detached) problems to two separate pickle files.

         `grids` is a mapping from grid name to GridMap. Each Problem's
         `grid_name` must appear as a key in `grids`. Uniqueness of grid
         names is enforced (duplicates would collide on load).
        ========================================================================
        """
        # Validate: every problem references a known grid
        Store._validate_grid_names(grids=grids)
        missing = {p.grid_name for p in problems} - set(grids.keys())
        if missing:
            raise ValueError(
                f'problems reference unknown grid names: {sorted(missing)}')
        # Pickle grids
        with open(path_grids, 'wb') as f:
            pickle.dump(grids, f, protocol=pickle.HIGHEST_PROTOCOL)
        # Pickle detached problems (light — no grid, no state cache)
        with open(path_problems, 'wb') as f:
            pickle.dump(problems, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(path_problems: str,
             path_grids: str,
             bind: bool = True
             ) -> tuple[list[ProblemGrid], dict[str, GridMap]]:
        """
        ========================================================================
         Load problems and grids from disk.

         When `bind` is True, each Problem is attached to its Grid using a
         shared StateCell cache per grid. When False, problems are returned
         detached — the caller can attach selectively.
        ========================================================================
        """
        with open(path_grids, 'rb') as f:
            grids: dict[str, GridMap] = pickle.load(f)
        with open(path_problems, 'rb') as f:
            problems: list[ProblemGrid] = pickle.load(f)
        if bind:
            Store.bind(problems=problems, grids=grids)
        return problems, grids

    @staticmethod
    def bind(problems: list[ProblemGrid],
             grids: dict[str, GridMap]) -> None:
        """
        ========================================================================
         Attach each Problem to its Grid, sharing one StateCell cache per
         distinct Grid across the batch.
        ========================================================================
        """
        caches: dict[str, dict] = {}
        for p in problems:
            grid = grids.get(p.grid_name)
            if grid is None:
                raise ValueError(
                    f'no grid named {p.grid_name!r} for problem '
                    f'{p.name!r}.')
            cache = caches.get(p.grid_name)
            if cache is None:
                cache = {c: StateCell(key=c) for c in grid}
                caches[p.grid_name] = cache
            p.attach(grid=grid, states=cache)

    @staticmethod
    def _validate_grid_names(grids: dict[str, GridMap]) -> None:
        """
        ========================================================================
         Validate: each grid's internal `name` matches its dict key.
        ========================================================================
        """
        for key, grid in grids.items():
            if grid.name != key:
                raise ValueError(
                    f'grid dict key {key!r} does not match '
                    f'grid.name {grid.name!r}.')
