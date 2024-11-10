from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class PathBasic(Generic[Node]):

    def get(self, goal: Node) -> list[Node]:
        return goal.path_from_start()
