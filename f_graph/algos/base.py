from f_graph.problems.i_2_one_to_one import ProblemOneToOne, NodePath
from f_graph.data.i_1_one_to_one import DataOneToOne
from f_graph.path.forward import PathForward
from f_ds.queues.i_0_base import QueueBase
from typing import Generic, TypeVar, Type
from abc import ABC

Node = TypeVar('Node', bound=NodePath)


class AlgoOneToOne(ABC, Generic[Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One path problems.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOneToOne,
                 type_queue: Type[QueueBase]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._data = DataOneToOne[Node](type_queue=type_queue)
        self._path = PathForward[Node](goal=problem.goal)
        self._search()

    @property
    def problem(self) -> ProblemOneToOne:
        """
        ========================================================================
         Return the shortest path One-to-One Problem.
        ========================================================================
        """
        return self._problem

    @property
    def data(self) -> DataOneToOne[Node]:
        """
        ========================================================================
         Return the Algo's Data (Generated and Explored).
        ========================================================================
        """
        return self._data

    @property
    def path(self) -> PathForward:
        """
        ========================================================================
         Return the Path-Manager of the shortest path problem.
        ========================================================================
        """
        return self._path

    def _search(self) -> None:
        """
        ========================================================================
         Search the shortest path from Start to Goal.
        ========================================================================
        """
        self._generate_node(node=self._problem.start)
        while self._data.generated:
            best = self._data.generated.pop()
            if best == self._problem.goal:
                self._path.set_valid()
                break
            self._explore_node(node=best)

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
