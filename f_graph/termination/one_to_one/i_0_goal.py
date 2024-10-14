from f_graph.termination.abc import TerminationABC
from f_graph.nodes.i_1_path import NodePath
from typing import TypeVar

Node = TypeVar('Node', bound=NodePath)


class TerminationGoal(TerminationABC):

    def __init__(self, goal: Node) -> None:
        self._goal = goal

    def can(self, node: Node) -> bool:
        return node == self._goal
