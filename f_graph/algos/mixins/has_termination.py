from enum import Enum
from f_abstract.mixins.has import Has
from f_graph.nodes.i_1_path import NodePath
from f_graph.termination.base import TerminationBase
from f_graph.termination.one_to_one.i_0_goal import TerminationGoal
from f_graph.termination.one_to_one.i_1_cache import TerminationCache
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class TypeTermination(Enum):
    """
    ============================================================================
     Enum-Class with Termination options.
    ============================================================================
    """
    GOAL = TerminationGoal
    CACHE = TerminationCache


class HasTermination(Has, Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Path-Algorithms with Termination test.
    ============================================================================
    """

    def __init__(self,
                 type_termination: TypeTermination,
                 **kwargs) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._termination = type_termination.value(**kwargs)

    @property
    def termination(self) -> TerminationBase:
        """
        ========================================================================
         Return the Termination object of the Algorithm.
        ========================================================================
        """
        return self._termination
