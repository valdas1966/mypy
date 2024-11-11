from f_graph.nodes.i_1_path import NodePath
from typing import TypeVar, Protocol

Node = TypeVar('Node', bound=NodePath)


class ProtocolData(Protocol[Node]):

    def mark_generated(self, node: Node) -> None:
        ...

    def mark_explored(self, node: Node) -> None:
        ...

    def is_generated(self, node: Node) -> bool:
        ...

    def is_explored(self, node: Node) -> bool:
        ...

    def is_active_goal(self, node: Node) -> bool:
        ...

    def remove_active_goal(self, goal: Node) -> None:
        ...

    def has_generated(self) -> bool:
        ...

    def has_active_goals(self) -> bool:
        ...
