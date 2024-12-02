# Config module of Path-Algorithms with Cache

from f_graph.path.config import (Problem, Ops, Queue, TProblem, TOps,
                                 TNode)
from f_graph.path.cache.components.data import Data
from f_graph.path.cache.components.path import Path

from typing import TypeVar

TPath = TypeVar('TPath', bound=Path)
TData = TypeVar('TData', bound=Data)
