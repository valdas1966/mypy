from typing import Protocol
from f_heuristic_search.problem_types.spp import SPP


class ProtocolAlgoSPP(Protocol):

    def __init__(self, spp: SPP) -> None:
        self._spp = spp

        