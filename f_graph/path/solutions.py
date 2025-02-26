from f_graph.path.path import Path
from f_graph.path.stats import StatsPath
from f_graph.path.node import NodePath as Node
from f_core.abstracts.dictable import Dictable
from f_core.mixins.validatable import Validatable
from f_graph.path.one_to_one.solution import SolutionOneToOne as Solution
from f_graph.path.one_to_one.state import StateOneToOne as State

class SolutionsPath(Dictable[Node, Solution], Validatable):
    """
    ========================================================================
     Solutions of Path-Problems.
    ========================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 sols: dict[Node, Solution],
                 order: list[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Dictable.__init__(self, data=sols)
        Validatable.__init__(self, is_valid=is_valid)
        self._elapsed: int = sum(sol.stats.elapsed for sol in sols.values())
        self._generated: int = sum(sol.stats.generated for sol in sols.values())
        self._explored: int = sum(sol.stats.explored for sol in sols.values())
        self._stats: dict[Node, StatsPath] = dict()
        self._paths: dict[Node, Path] = dict()
        self._states: dict[Node, State] = dict()
        self._order: list[Node] = order
        for node, sol in sols.items():
            self._stats[node] = sol.stats
            self._paths[node] = sol.path
            self._states[node] = sol.state
    @property
    def elapsed(self) -> int:
        """
        ========================================================================
         Return the overall elapsed time of all solutions.
        ========================================================================
        """
        return self._elapsed

    @property
    def generated(self) -> int:
        """
        ========================================================================
         Return the overall number of generated nodes of all solutions.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the overall number of explored nodes of all solutions.
        ========================================================================
        """
        return self._explored

    @property
    def stats(self) -> dict[Node, StatsPath]:
        """
        ========================================================================
         Return the stats of all solutions.
        ========================================================================
        """
        return self._stats

    @property
    def paths(self) -> dict[Node, Path]:
        """
        ========================================================================
         Return the paths of all solutions.
        ========================================================================
        """
        return self._paths
    
    @property
    def states(self) -> dict[Node, State]:
        """
        ========================================================================
         Return the states of all solutions.
        ========================================================================
        """
        return self._states
    
    @property
    def order(self) -> list[Node]:
        """
        ========================================================================
         Return the order of the solutions.
        ========================================================================
        """
        return self._order

