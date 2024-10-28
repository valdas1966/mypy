from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class DataABC(Generic[Node]):
    pass
