from f_graph.path_finding.algo import Algo as AlgoPath
from f_graph.path_finding.cache.config import Problem, Path, Ops, Data, Node


class Algo(AlgoPath[Problem, Path, Data, Ops]):
    """
    ============================================================================
     Path-Finding Algorithm with Cache object.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 data: Data,
                 ops: Ops,
                 path: Path,
                 name: str = 'Algorithm-Path-Cache'):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self,
                          problem=problem,
                          data=data,
                          ops=ops,
                          path=path,
                          name=name)

    def _process_best(self) -> None:
        """
        ========================================================================
         Process best generated node.
        ========================================================================
        """
        if self._best_is_goal() or self._best_is_cached():
            self._data.remove_active_goal(goal=self._best)

    def _best_is_cached(self) -> bool:
        """
        ========================================================================
         Return True if the Best-Node is cached.
        ========================================================================
        """
        return self._data.is_cached(self._best)