# Config module of Path-Algorithms

from f_graph.path.problem import ProblemPath
from f_graph.path.components.path import Path
from f_graph.path.components.state import State, Queue
from f_graph.path.components.ops import Ops
from f_graph.path.node import NodePath
from typing import TypeVar

TProblem = TypeVar('TProblem', bound=ProblemPath)
TPath = TypeVar('TPath', bound=Path)
TData = TypeVar('TData', bound=State)
TOps = TypeVar('TOps', bound=Ops)
TQueue = TypeVar('TQueue', bound=Queue)
TNode = TypeVar('TNode', bound=NodePath)
