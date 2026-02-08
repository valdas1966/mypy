from __future__ import annotations
from f_hs.ds.path import Path
from f_graph.old_path.core.stats import StatsPath
from f_hs.ds._old_node import NodePath as Node
from f_core.mixins.dictable.main import Dictable
from f_core.mixins.validatable.main import Validatable
from f_graph.old_path.algos.one_to_one.solution import SolutionOneToOne
from f_graph.old_path.algos.one_to_one.state import StateOneToOne as State


class SolutionsPath(Dictable[Node, SolutionOneToOne], Validatable):
    """
    ========================================================================
     Solutions of Path-Problems.
    ========================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 sols: dict[Node, SolutionOneToOne]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Dictable.__init__(self, data=sols)
        Validatable.__init__(self, is_valid=is_valid)
        self._sols = sols
        self._elapsed: int = sum(sol.stats.elapsed for sol in sols.values())
        self._generated: int = sum(sol.stats.generated for sol in sols.values())
        self._explored: int = sum(sol.stats.explored for sol in sols.values())
        self._stats: dict[Node, StatsPath] = dict()
        self._paths: dict[Node, Path] = dict()
        self._states: dict[Node, State] = dict()
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
         Return the overall number of generated old_nodes of all solutions.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> int:
        """
        ========================================================================
         Return the overall number of explored old_nodes of all solutions.
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
         Return the state of all solutions.
        ========================================================================
        """
        return self._states
    
    @property
    def sols(self) -> dict[Node, SolutionOneToOne]:
        """
        ========================================================================
         Return the solutions of all solutions.
        ========================================================================
        """
        return self._sols

    def update(self, other: SolutionsPath) -> None:
        """
        ========================================================================
         Update the solutions.
         [NOT PERFECT]
        ========================================================================
        """
        self._elapsed += other.elapsed
        self._generated += other.generated
        self._explored += other.explored
        for node, sol in other.sols.items():
            self._sols[node] = sol
            self._stats[node] = sol.stats
            self._paths[node] = sol.path
            self._states[node] = sol.state  

