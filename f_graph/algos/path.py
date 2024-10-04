from f_graph.problems.i_1_path import ProblemPath, NodePath
from f_graph.data.i_0_path import DataPath
from f_graph.paths.i_0_base import PathBase
from typing import Generic, TypeVar, Type
from abc import ABC, abstractmethod

Problem = TypeVar('Problem', bound=ProblemPath)
Node = TypeVar('Node', bound=NodePath)
Data = TypeVar('Data', bound=DataPath)
Path = TypeVar('Path', bound=PathBase)


class AlgoPath(ABC, Generic[Problem, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 data: Data,
                 type_path: Type[PathBase]
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._data = data
        self._path = type_path(problem=problem)
        self._search()

    @property
    def problem(self) -> Problem:
        """
        ========================================================================
         Return the shortest paths One-to-One Problem.
        ========================================================================
        """
        return self._problem

    @property
    def data(self) -> Data:
        """
        ========================================================================
         Return the Algo Data (Generated and Explored).
        ========================================================================
        """
        return self._data

    @property
    def path(self) -> Path:
        """
        ========================================================================
         Return a Path founded in the Algo.
        ========================================================================
        """
        return self._path

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
