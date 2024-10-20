from enum import Enum
from f_abstract.mixins.has import Has
from f_graph.data.i_0_path import DataPath, NodePath
from f_graph.data.i_1_one_to_one import DataOneToOne
from f_graph.data.i_2_one_to_many import DataOneToMany
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class CL(Enum):
    ONE_TO_ONE = DataOneToOne
    ONE_TO_MANY = DataOneToMany


class HasData(Has, Generic[Node]):

    def __init__(self, cl: CL) -> None:
        self._data = cl.value()
