from __future__ import annotations
from f_graph.path.problem import ProblemPath, Graph, Node, dataclass
from f_graph.path.single.problem import ProblemSingle
from typing import Iterable


@dataclass(frozen=True)
class ProblemMulti(ProblemPath):
    """
    ============================================================================
     Path-Problem with Multiple-Goals.
    ============================================================================
    """

    goals: set[Node]

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goals: Iterable[Node]) -> None:
        """
        ========================================================================
         Init Attributes.
        ========================================================================
        """
        ProblemPath.__init__(self, graph=graph, start=start)
        object.__setattr__(self, 'goals', set(goals))

    def to_singles(self) -> tuple[ProblemSingle, ...]:
        """
        ========================================================================
         Convert a ProblemMulti into a Tuple of ProblemSingle.
        ========================================================================
        """
        return tuple(ProblemSingle(graph=self.graph,
                                   start=self.start,
                                   goal=goal)
                     for goal
                     in self.goals)

    def clone(self) -> ProblemMulti:
        """
        ========================================================================
         Return a Cloned problem.
        ========================================================================
        """
        graph = self.graph.clone()
        start = graph.node_from_uid(uid=self.start.uid)
        goals = {graph.node_from_uid(uid=goal.uid) for goal in self.goals}
        return ProblemMulti(graph=graph, start=start, goals=goals)

    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-Representation.
        ========================================================================
        """
        return (f'{self.graph._grid.shape()} {self.start.uid} -> ['
                f'{', '.join([str(goal.uid) for goal in self.goals])}]')

    @classmethod
    def gen_3x3(cls) -> ProblemMulti:
        """
        ========================================================================
         Return a Generated-Problem of 3x3 Grid and 2 Goals.
        ========================================================================
        """
        graph = Graph.gen_3x3(type_node=Node)
        start = graph[0, 0]
        goals = {graph[0, 2], graph[2, 2]}
        return ProblemMulti(graph=graph, start=start, goals=goals)
