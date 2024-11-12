from f_graph.nodes.i_1_path import NodePath
from typing import Protocol, TypeVar

Node = TypeVar('Node', bound=NodePath)


class ProtocolOps(Protocol[Node]):

    def generate(self, node: Node, parent: Node = None) -> None:
        ...

    def explore(self, node: Node) -> None:
        ...
