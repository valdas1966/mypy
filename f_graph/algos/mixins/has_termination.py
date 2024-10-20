from enum import Enum
from f_abstract.mixins.has import Has
from f_graph.nodes.i_1_path import NodePath
from f_graph.termination.one_to_one.i_0_goal import TerminationGoal
from f_graph.termination.one_to_one.i_1_cache import TerminationCache
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class HasTermination(Has, Generic[Node]):

    @staticmethod
    def CL(self) -> Enum:
        return Enum(TerminationGoal, TerminationCache)

    def __init__(self,
                 goal: Node,
                 cache: set[Node] = None) -> None:
        self._goal = goal
        self._cache = cache or set()

    def can_terminate(self) -> bool: