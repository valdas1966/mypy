from f_graph.problems.i_1_path import ProblemPath, NodePath
from f_graph.termination.base import TerminationBase
from f_graph.data.i_0_path import DataPath
from f_graph.paths.i_0_base import PathBase
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

Problem = TypeVar('Problem', bound=ProblemPath)
Termination = TypeVar('Termination', bound=TerminationBase)
Node = TypeVar('Node', bound=NodePath)
Data = TypeVar('Data', bound=DataPath)
Path = TypeVar('Path', bound=PathBase)


class AlgoPath(ABC, Generic[Problem, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """

    def __init__(self, problem: Problem) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._data = self._create_data()
        self._path = self._create_path()
        self._termination = self._create_termination()
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
    def termination(self) -> Termination:
        """
        ========================================================================
         Return the Termination checker of the Search process.
        ========================================================================
        """
        return self._termination

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
    def _create_termination(self) -> Termination:
        pass

    @abstractmethod
    def _create_data(self) -> Data:
        pass

    @abstractmethod
    def _create_path(self) -> Path:
        pass

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
