from f_graph.path.components.data import Data
from f_graph.path.problem import ProblemGrid as Problem, NodeCell
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeCell)


class Ops(Generic[Node]):
    """
    ============================================================================
     Operations object of Path-Finding Algorithms.
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

    def generate(self, node: Node, parent: Node = None) -> None:
        """
        ========================================================================
         Generate a Node.
        ========================================================================
        """
        node.parent = parent
        self._data.mark_generated(node=node)

    def explore(self, node: Node) -> None:
        """
        ========================================================================
         Explore a Node (process its children).
        ========================================================================
        """
        children = self._problem.graph.neighbors(node)
        for child in children:
            self._process_child(child=child, parent=node)
        self._data.mark_explored(node=node)

    def _process_child(self, child: Node, parent: Node) -> None:
        """
        ========================================================================
         Process a Child-Node.
        ========================================================================
        """
        if self._data.is_explored(node=child):
            return
        if self._data.is_generated(node=child):
            return
        self.generate(node=child, parent=parent)
