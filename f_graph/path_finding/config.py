# Config module of Path-Algorithms

from f_graph.path_finding.problem import Problem
from f_graph.path_finding.components.path import Path
from f_graph.path_finding.components.data import Data, Queue
from f_graph.path_finding.components.ops import Ops
from f_graph.path_finding.nodes.i_1_path import NodePath
from typing import TypeVar

TProblem = TypeVar('TProblem', bound=Problem)
TPath = TypeVar('TPath', bound=Path)
TData = TypeVar('TData', bound=Data)
TOps = TypeVar('TOps', bound=Ops)
TQueue = TypeVar('TQueue', bound=Queue)
TNode = TypeVar('TNode', bound=NodePath)
