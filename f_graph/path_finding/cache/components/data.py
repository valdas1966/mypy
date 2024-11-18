from f_graph.path_finding.config import Problem, Queue, Node, Data as DataPath
from typing import Type


class Data(DataPath[Node]):

    def __init__(self,
                 problem: Problem,
                 cache: set[Node],
                 type_queue: Type[Queue]):
        DataPath.__init__(self, problem=problem, type_queue=type_queue)
        self._cache = cache

    def is_cached(self, node: Node) -> bool:
        return node in self._cache
