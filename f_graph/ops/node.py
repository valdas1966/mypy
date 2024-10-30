from f_graph.problems.i_1_path import ProblemPath
from f_graph.data.i_0_abc import DataABC, Node
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Data = TypeVar('Data', bound=DataABC)


class OpsNode(Generic[Problem, Data, Node]):
    """
    ============================================================================
     Class for Node's Operations in PathFinding-Algorithms.
    ============================================================================
    """

    def __init__(self, problem: Problem, data: Data) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._data = data

    def generate(self,
                 node: Node,
                 parent: Node = None) -> None:
        """
        ========================================================================
         Generate a Node (Set parent and Mark as generated).
        ========================================================================
        """
        node.parent = parent
        self._data.mark_generated(node=node)

    def explore(self, node: Node) -> None:
        """
        ========================================================================
         Explore the Node (generate all node's children).
        ========================================================================
        """
        children = self._problem.graph.neighbors(node)
        for child in children:
            self._process_child(child=child, parent=node)
        self._data.mark_explored(node=node)

    def try_update(self,
                   child: Node,
                   parent: Node) -> None:
        """
        ========================================================================
         No Update on Default.
        ========================================================================
        """
        pass

    def _process_child(self,
                       child: Node,
                       parent: Node) -> None:
        """
        ========================================================================
         Determine a Child of an Explored-Node should be Generated or Updated.
        ========================================================================
        """
        if self._data.is_explored(node=child):
            return
        if self._data.is_generated(node=child):
            self.try_update(child=child, parent=parent)
        else:
            self.generate(node=child, parent=parent)
