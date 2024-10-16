from f_graph.problems.i_2_one_to_many import ProblemOneToMany
from f_graph.data.i_0_path import DataPath, NodePath, QueueBase
from typing import TypeVar, Type

Node = TypeVar('Node', bound=NodePath)


class DataOneToMany(DataPath[Node]):
    """
    ============================================================================
     Class of Data for One-to-Many Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOneToMany,
                 type_queue: Type[QueueBase],
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataPath.__init__(self, type_queue=type_queue)
        self._goals_active = problem.goals

    @property
    def goals_active(self) -> set[Node]:
        """
        ========================================================================
         Return current Active-Goals (not found paths to them yet).
        ========================================================================
        """
        return self._goals_active
