from f_heuristic_search.algos.data.i_0_base import DataBase
from f_data_structure.collections.i_1_queue import QueueBase
from f_data_structure.nodes.i_0_base import NodeBase
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeBase)
Queue = TypeVar('Queue', bound=QueueBase)


class Data(Generic[Queue, Node], DataBase):

    def __init__(self) -> None:
        self._generated = Queue[Node]()
        self._explored = set[Node]()

    @property
    def generated(self) -> Queue[Node]:
        return self._generated

    @property
    def explored(self) -> set[Node]:
        return self._explored
