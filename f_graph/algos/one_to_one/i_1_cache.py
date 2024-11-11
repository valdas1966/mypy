from f_graph.algos.one_to_one.i_0_abc import (AlgoOneToOneABC, Problem, Data,
                                              OpsNode, Node, Queue)
from f_graph.search.cache.cache import Cache
from typing import Type


class AlgoOneToOneCache(AlgoOneToOneABC[Problem, Data, OpsNode, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """
    def __init__(self,
                 problem: Problem,
                 type_queue: Type[Queue],
                 cache: set[Node],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._cache = Cache(cache=cache)
        AlgoOneToOneABC.__init__(self,
                                 problem=problem,
                                 type_queue=type_queue,
                                 name=name)

    def _can_terminate(self, best: Node) -> bool:
        """
        ========================================================================
         Terminate the Search if the Best-Generated-Node is a Goal.
        ========================================================================
        """
        return best == self._problem.goal or best in self._cache

    def _construct_path(self, best: Node) -> None:
        """
        ========================================================================
         Construct an Optimal-Path from Start to the Best-Node (the Goal).
        ========================================================================
        """
        path_start_to_best = best.path_from_start()
        path_best_to_goal = self._cache.path_to_goal(node=best)[1:]
        self._path = path_start_to_best + path_best_to_goal
