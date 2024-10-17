from f_graph.algos.i_0_path import AlgoPath, ProblemPath, NodePath
from abc import ABC
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Node = TypeVar('Node', bound=NodePath)


class AlgoCache(AlgoPath[Problem, Node], ABC):

    def __init__(self,
                 problem: Problem,
                 cache: set[Node] = None) -> None:
        self._cache = cache or set()
        AlgoPath.__init__(self, problem=problem)

    @property
    def cache(self) -> set[Node]:
        return self._cache
