from f_graph.problems.i_1_path import ProblemPath, NodePath
from f_graph.data.i_0_path import DataPath
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Data = TypeVar('Data', bound=DataPath)
Node = TypeVar('Node', bound=NodePath)


class OpsPath(Generic[Problem, Data, Node]):
    """
    ============================================================================
     Class for Node's Operations in PathFinding-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 data: Data) -> None:
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
            return
        self.generate(node=child, parent=parent)
