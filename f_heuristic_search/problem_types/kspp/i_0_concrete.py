from f_heuristic_search.nodes.i_1_g import NodeG as Node
from f_heuristic_search.graphs.graph import Graph


class KSPP:
    """
    ============================================================================
     Represents K-Shortest-Path-Problems with the same Start.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goals: tuple[Node, ...]) -> None:
        self._graph = graph
        self._start = start
        self._goals = goals
        self._goals_active = set(goals)

    @property
    def graph(self) -> Graph:
        return self._graph

    @property
    def start(self) -> Node:
        return self._start

    @property
    def goals(self) -> tuple[Node, ...]:
        return self._goals

    @property
    def goals_active(self) -> set[Node]:
        return self._goals_active

    def remove_goal_active(self, goal: Node) -> None:
        """
        ========================================================================
         Remove Goal from the Active-List (after search reached it).
        ========================================================================
        """
        self._goals_active.remove(element=goal)
