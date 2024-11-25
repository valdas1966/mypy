# Config module of Path-Algorithms

from f_graph.path_finding.components.problem import Problem, NodePath
from f_graph.path_finding.components.path import Path
from f_graph.path_finding.components.data import Data, Queue
from f_graph.path_finding.components.ops import Ops
from typing import TypeVar

TProblem = TypeVar('TProblem', bound=Problem)
TPath = TypeVar('TPath', bound=Path)
TData = TypeVar('TData', bound=Data)
TOps = TypeVar('TOps', bound=Ops)
TNode = TypeVar('TNode', bound=NodePath)
