from abc import ABC
from typing import Generic, TypeVar
from f_graph.nodes.i_1_path import NodePath

Node = TypeVar('Node', bound=NodePath)

class PathBase(ABC, Generic[Node]):

    def __init__(self):
        pass