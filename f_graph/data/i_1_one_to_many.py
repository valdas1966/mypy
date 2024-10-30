from f_graph.data.i_0_abc import DataABC, Queue, Node
from typing import Type, Sequence


class DataOneToMany(DataABC[Node]):
    """
    ============================================================================
     Class of Data for One-to-Many Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 type_queue: Type[Queue],
                 goals: Sequence[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataABC.__init__(self, type_queue=type_queue)
        self._goals_active: set[Node] = set(goals)

    @property
    def goals_active(self) -> set[Node]:
        """
        ========================================================================
         Return current Active-Goals (not found paths to them yet).
        ========================================================================
        """
        return self._goals_active
