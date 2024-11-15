from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Path(Generic[Node]):

    def __init__(self, goals: set[Node]) -> None:
        self._goals = goals

    def get(self, goal: Node) -> list[Node]:
        return self._goals[goal].path_from_start()
