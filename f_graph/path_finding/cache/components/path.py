from f_graph.path_finding.components.path import Path as PathFinding, NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Path(Generic[Node], PathFinding[Node]):

    def get(self, goal: Node) -> list[Node]:
        pass
