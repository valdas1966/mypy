from f_heuristic_search.problem_types.spp import SPP


class SPPAble(SPP):

    def __init__(self, spp: SPP) -> None:
        self._grid = spp.grid
        self._start = spp.start
        self._goal = spp.goal
        self._is_path_found = None

    @property
    def name(self) -> str:
        return f'{self._start.name} -> {self._goal.name}'

    @property
    def is_path_found(self) -> bool:
        return self._is_path_found

    def search(self) -> None:
        raise NotImplementedError()
