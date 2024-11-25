from f_graph.nodes.i_1_path import NodePath
from f_graph.path_finding.protocols.problem import Problem
from f_ds.queues.i_0_base import QueueBase as Queue
from typing import TypeVar, Type, Protocol

Node = TypeVar('Node', bound=NodePath)


class Data(Protocol[Node]):
    """
    ============================================================================
     Protocol of Data objects in the Path-Finding Algorithms.
    ============================================================================
    """

    def mark_generated(self, node: Node) -> None:
        """
        ========================================================================
         Mark a Node as Generated.
        ========================================================================
        """

    def mark_explored(self, node: Node) -> None:
        """
        ========================================================================
         Mark a Node as Explored.
        ========================================================================
        """

    def is_generated(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node is already Generated.
        ========================================================================
        """

    def is_explored(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node is already Explored.
        ========================================================================
        """
        ...

    def pop_generated(self) -> Node:
        """
        ========================================================================
         Pop best generated node.
        ========================================================================
        """

    def is_active_goal(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if a Node is an Active-Goal.
        ========================================================================
        """

    def remove_active_goal(self, goal: Node) -> None:
        """
        ========================================================================
         Remove a Goal from the Active-Goals set.
        ========================================================================
        """

    def has_generated(self) -> bool:
        """
        ========================================================================
         Return True if there has more Nodes in the Generated list.
        ========================================================================
        """

    def has_active_goals(self) -> bool:
        """
        ========================================================================
         Return True if there has more Goals in the Active-Goals set.
        ========================================================================
        """
