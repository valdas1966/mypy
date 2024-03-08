from typing import Type
from f_heuristic_search.problem_types.spp import SPP, Graph, Node


class SPPLookup(SPP):
    """
    ============================================================================
     Shortest-Path-Problem in Heuristic Search with a Lookup property.
    ============================================================================
    """

    def __init__(self,
                 graph: Type[Graph],
                 start: Type[Node],
                 goal: Type[Node],
                 heuristics: dict[Type[Node], int] = dict(),
                 lookup: dict[Type[Node], list[Type[Node]]] = dict()) -> None:
        SPP.__init__(self, graph, start, goal, heuristics)
        self._lookup = lookup

    @property
    # Accurate Distance from SPP-Nodes to the Goal
    def lookup(self) -> dict[Type[Node], int]:
        return self._lookup
