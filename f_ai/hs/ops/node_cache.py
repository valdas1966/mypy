from f_ai.hs.ops.node import OpsNodeHS, Problem, DataOneToOne, Node
from f_graph.path.ds.cache import Cache
from typing import Callable


class OpsNodeHSCache(OpsNodeHS[Problem, Node]):

    def __init__(self,
                 problem: Problem,
                 data: DataOneToOne,
                 heuristics: Callable[[Node], int],
                 cache: Cache) -> None:
        OpsNodeHS.__init__(self,
                           problem=problem,
                           data=data,
                           heuristics=self._combine_heuristics(h=heuristics,
                                                               cache=cache))

    def _combine_heuristics(self,
                            h: Callable[[Node], int],
                            cache: Cache[Node]) -> Callable[[Node], int]:
        def func(node: Node) -> int:
            if node in cache:
                return cache.accurate_distance_to_goal(node=node)
            return h(node)
        return func
