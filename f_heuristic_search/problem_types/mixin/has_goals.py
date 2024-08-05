from f_data_structure.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class HasGoals(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Problems with multiple Goals.
    ============================================================================
    """

    def __init__(self, goals: tuple[Node, ...]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goals = goals
        self._goals_active = set(goals)

    @property
    def goals(self) -> tuple[Node, ...]:
        return self._goals

    @property
    def goals_active(self) -> set[Node]:
        return self._goals_active

    def remove_goal_active(self, goal: Node) -> bool:
        """
        ========================================================================
         Remove list given Goal from an Active-Goals set.
        ========================================================================
        """
        self._goals_active.remove(goal)
