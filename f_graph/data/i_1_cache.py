from f_graph.data.i_0_path import DataPath, NodePath, QueueBase
from typing import TypeVar, Type

Node = TypeVar('Node', bound=NodePath)


class DataCache(DataPath[Node]):

    def __init__(self,
                 type_queue: Type[QueueBase],
                 cache: set[Node] = None) -> None:
        self._cache = cache if cache else set()
        DataPath.__init__(self, type_queue=type_queue)

    @property
    def cache(self) -> set[Node]:
        return self._cache
