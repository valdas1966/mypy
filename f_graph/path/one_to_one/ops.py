from f_graph.path.one_to_one.state import StateOneToOne as State
from f_graph.path.problem import ProblemPath as Problem
from f_graph.path.heuristic import Heuristic, Node
from f_graph.path.boundary import Boundary
from f_graph.path.cache import Cache
from collections import Counter
from enum import Enum, auto


class TypeCounter(Enum):
    """
    ============================================================================
     Type of Counter (for logging).
    ============================================================================
    """
    GENERATED = auto()
    EXPLORED = auto()


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
                 boundary: Boundary,
                 heuristic: Heuristic) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._problem = problem
        self._state = state
        self._cache = cache
        self._boundary = boundary
        self._heuristic = heuristic
        self._counter = Counter({TypeCounter.GENERATED: 0,
                                 TypeCounter.EXPLORED: 0})

    @property
    def counter(self) -> Counter:
        """
        ========================================================================
         Return the counter for logging.
        ========================================================================
        """
        return self._counter

    def generate_node(self, node: Node, parent: Node = None) -> None:
        """
        ========================================================================
         Generate a Node.
        ========================================================================
        """
        node.parent = parent
        if node in self._cache:
            node.h = len(self._cache[node]) - 1
            node.is_cached = True
        elif node in self._boundary:
            node.h = max(self._heuristic(node=node),
                         self._boundary[node])
            # node.is_bounded = self._boundary[node] > self._heuristic(node=node)
            node.is_bounded = True
        else:
            node.h = self._heuristic(node=node)
        self._state.generated.push(item=node)
        self._counter[TypeCounter.GENERATED] += 1

    def explore_node(self, node: Node) -> None:
        """
        ========================================================================
         Explore a Node (process its children).
        ========================================================================
        """
        children = self._problem.graph.children(node)
        for child in children:
            self._process_child(child=child, parent=node)
        self._state.explored.add(node)
        self._counter[TypeCounter.EXPLORED] += 1

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
            self.generate_node(node=child, parent=parent)
