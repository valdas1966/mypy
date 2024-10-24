from f_graph.algos.mixins.has_problem import HasProblem, ProblemPath
from f_graph.algos.mixins.has_data import HasData, TypeData, TypeQueue
from f_graph.algos.mixins.has_path import HasPath
from f_graph.nodes.i_1_path import NodePath
from f_abstract.mixins.nameable import Nameable
from typing import Generic, TypeVar
from abc import abstractmethod

Problem = TypeVar('Problem', bound=ProblemPath)
Node = TypeVar('Node', bound=NodePath)


class AlgoPath(Generic[Problem, Node],
               Nameable,
               HasProblem,
               HasData[Node],
               HasPath[Node]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_data: TypeData,
                 type_queue: TypeQueue,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        HasProblem.__init__(self, problem=problem)
        HasData.__init__(self, type_data=type_data, type_queue=type_queue)
        HasPath.__init__(self)

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
