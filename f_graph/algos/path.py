from f_graph.problems.i_1_path import ProblemPath, NodePath
from f_graph.data.i_0_path import DataPath
from f_ds.queues.i_0_base import QueueBase
from typing import Generic, TypeVar, Type
from abc import ABC, abstractmethod

Node = TypeVar('Node', bound=NodePath)
Problem = TypeVar('Problem', bound=ProblemPath)
Data = TypeVar('Data', bound=DataPath)


class AlgoPath(ABC, Generic[Node, Problem, Data]):
    """
    ============================================================================
     Base-Algorithm for One-To-One path problems.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_data: Type[Data],
                 type_queue: Type[QueueBase]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._data = type_data(type_queue=type_queue)
        self._is_found = False
        self._search()

    @property
    def problem(self) -> Problem:
        """
        ========================================================================
         Return the shortest path One-to-One Problem.
        ========================================================================
        """
        return self._problem

    @property
    def data(self) -> Data:
        """
        ========================================================================
         Return the Algo's Data (Generated and Explored).
        ========================================================================
        """
        return self._data

    @abstractmethod
    def _search(self) -> None:
        """
        ========================================================================
         Execute the search process.
        ========================================================================
        """
        pass

    def _explore_node(self, node: Node) -> None:
        """
        ========================================================================
         Explore the Node (generate all node's children).
        ========================================================================
        """
        children = self._problem.graph.neighbors(node)
        for child in children:
            if child in self._data.explored:
                continue
            if child in self._data.generated:
                self._try_update_node(node=child, parent=node)
            else:
                self._generate_node(node=child, parent=node)
        self._data.explored.add(node)

    def _try_update_node(self, node: Node, parent: Node) -> None:
        """
        ========================================================================
         Try update generated Node with new relevant info.
        ========================================================================
        """
        pass

    def _generate_node(self,
                       node: Node,
                       parent: Node = None) -> None:
        """
        ========================================================================
         Generate a Node (set parent and add to generated list).
        ========================================================================
        """
        node.parent = parent
        self._data.generated.push(node)
