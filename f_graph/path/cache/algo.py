from f_graph.path.algo import AlgoPath as AlgoPath
from f_graph.path.cache.config import (Data, Queue,
                                       TProblem, TPath, TData, TOps, TNode)
from typing import Generic, Type


class AlgoCache(Generic[TProblem, TPath, TOps, TData, TNode],
                AlgoPath[TProblem, TPath, TData, TOps, TNode]):
    """
    ============================================================================
     Path-Finding Algorithm with Cache object.
    ============================================================================
    """

    def __init__(self,
                 problem: TProblem,
                 type_queue: Type[Queue],
                 cache: set[TNode],
                 name: str = 'Algorithm-Path-Cache'):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._cache = cache
        AlgoPath.__init__(self,
                          problem=problem,
                          type_queue=type_queue,
                          name=name)

    def _create_state(self) -> TData:
        """
        ========================================================================
         Create a Data object.
        ========================================================================
        """
        return Data(problem=self._input,
                    cache=self._cache,
                    type_queue=self._type_queue)

    def _is_path_found(self) -> bool:
        """
        ========================================================================
         Return True if the Best-Generated Node is a Goal or in the Cache.
        ========================================================================
        """
        return self._best_is_goal() or self._best_is_cached()

    def _best_is_cached(self) -> bool:
        """
        ========================================================================
         Return True if the Best-Node is cached.
        ========================================================================
        """
        return self._data.is_cached(self._best)
