from f_heuristic_search.problem_types.spp import SPP


class SPPAble:
    """
    ============================================================================
     Desc: Mixin for SPP-Algorithms.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. spp : SPP (Shortest Path Problem).
        2. is_path_found : bool (True if their is a path from Start to Goal).
    ============================================================================
    """

    def __init__(self, spp: SPP) -> None:
        self._spp = spp
        self._is_path_found = None

    @property
    def spp(self) -> SPP:
        return self._spp

    @property
    def is_path_found(self) -> bool:
        return self._is_path_found
