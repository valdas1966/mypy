from f_ds.protocols.queue import ProtocolQueue
from f_graph.nodes.i_1_path import NodePath
from collections.abc import Collection
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Data(Generic[Node]):
    """
    ============================================================================
     Data object of Path-Finding Algorithms.
    ============================================================================
    """

    def __init__(self,
                 generated: ProtocolQueue[Node],
                 goals: Collection[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._generated: ProtocolQueue[Node] = generated
        self._explored: set[Node] = set()
        self._goals_active: set[Node] = set(goals)

    def mark_generated(self, node: Node) -> None:
        """
        ========================================================================
         Mark a Node as Generated.
        ========================================================================
        """
        self._generated.push(item=node)

    def mark_explored(self, node: Node) -> None:
        """
        ========================================================================
         Mark a Node as Explored.
        ========================================================================
        """
        self._explored.add(node)

    def is_generated(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node was already Generated.
        ========================================================================
        """
        return node in self._generated

    def is_explored(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node was already Explored.
        ========================================================================
        """
        return node in self._explored

    def pop_generated(self) -> Node:
        """
        ========================================================================
         Pop best generated node.
        ========================================================================
        """
        return self._generated.pop()

    def is_active_goal(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node is an Active-Goal.
        ========================================================================
        """
        return node in self._goals_active

    def remove_active_goal(self, goal: Node) -> None:
        """
        ========================================================================
         Remove a Goal from the Active-Goals set.
        ========================================================================
        """
        self._goals_active.remove(goal)

    def has_generated(self) -> bool:
        """
        ========================================================================
         Return True if the Generated list has more Nodes.
        ========================================================================
        """
        return bool(self._generated)

    def has_active_goals(self) -> bool:
        """
        ========================================================================
         Return True if the Active-Goals set has more Goals.
        ========================================================================
        """
        return bool(self._goals_active)
