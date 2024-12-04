# Config module of Path-Algorithms

from f_graph.path.problem import ProblemGrid
from f_graph.path.components.path import Path
from f_graph.path.components.data import Data, Queue
from f_graph.path.components.ops import Ops
from f_graph.path.node import NodePath
from typing import TypeVar

TProblem = TypeVar('TProblem', bound=ProblemGrid)
TPath = TypeVar('TPath', bound=Path)
TData = TypeVar('TData', bound=Data)
TOps = TypeVar('TOps', bound=Ops)
TQueue = TypeVar('TQueue', bound=Queue)
TNode = TypeVar('TNode', bound=NodePath)
