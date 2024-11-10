from f_graph.nodes.i_1_path import NodePath
from f_graph.problems.i_1_path import ProblemPath
from f_ds.queues.i_0_base import QueueBase as Queue
from typing import Generic, TypeVar, Type

Problem = TypeVar('Problem', bound=ProblemPath)
Node = TypeVar('Node', bound=NodePath)


class DataPath(Generic[Problem, Node]):
    """
    ============================================================================
     ABC of Data objects for Path-Algorithms (Generated and Explored sets).
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[Queue]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._generated: Queue[Node] = type_queue()
        self._explored: set[Node] = set()
        self._goals_active: set[Node] = problem.goals

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
         Return True if the Node was Generated.
        ========================================================================
        """
        return node in self._generated

    def is_explored(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Node was Explored.
        ========================================================================
        """
        return node in self._explored

    def remove_goal_active(self, goal: Node) -> None:
        """
        ========================================================================
         Remove a Goal from an Active-Goals set.
        ========================================================================
        """
        self._goals_active.remove(goal)
