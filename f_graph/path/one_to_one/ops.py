from f_graph.path.one_to_one.problem import ProblemOneToOne as Problem, Node
from f_graph.path.one_to_one.state import StateOneToOne as State
from f_graph.path.one_to_one.cache import Cache
from typing import Callable


class OpsOneToOne:
    """
    ============================================================================
     Operations object of Path-Finding Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 state: State,
                 cache: Cache,
                 heuristic: Callable[[Node], int]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._state = state
        self._cache = cache
        self._heuristic = heuristic

    def generate(self, node: Node, parent: Node = None) -> None:
        """
        ========================================================================
         Generate a Node.
        ========================================================================
        """
        node.parent = parent
        if node in self._cache:
            node.h = self._cache[node].distance()
            node.is_cached = True
        else:
            self._set_heuristic(node)
        self._state.generated.push(item=node)

    def explore(self, node: Node) -> None:
        """
        ========================================================================
         Explore a Node (process its children).
        ========================================================================
        """
        children = self._problem.graph.neighbors(node)
        for child in children:
            self._process_child(child=child, parent=node)
        self._state.explored.add(node)

    def _process_child(self, child: Node, parent: Node) -> None:
        """
        ========================================================================
         Process a Child-Node.
        ========================================================================
        """
        if child in self._state.explored:
            return
        if child in self._state.generated:
            if child.is_better_parent(parent=parent):
                child.parent = parent
        else:
            self.generate(node=child, parent=parent)

    def _set_heuristic(self, node: Node) -> None:
        """
        ========================================================================
         Set the heuristic of the node.
        ========================================================================
        """
        node.h = self._heuristic(node) if self._heuristic else None
