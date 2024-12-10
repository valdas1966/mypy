from f_graph.path.single.components.problem import ProblemPath as Problem
from f_graph.path.node import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Solution(Generic[Node]):
    """
    ============================================================================
     Path object (the output) of Path-Algorithms.
    ============================================================================
    """

    def __init__(self, problem: Problem) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._paths: dict[Node, list[Node]] = dict()

    def construct(self, goal: Node) -> None:
        """
        ========================================================================
         Construct an Optimal-Path from the Start to a given Goal.
        ========================================================================
        """
        node = self._problem.graph.node_from_uid(uid=goal.uid)
        self._paths[goal] = node.path_from_start()

    def get(self, goal: Node) -> list[Node]:
        """
        ========================================================================
         Return an Optimal-Path from Start to the received Goal.
        ========================================================================
        """
        return self._paths[goal]
