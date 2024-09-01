from f_graph.problems.i_2_one_to_many import ProblemOneToMany
from f_graph.data.i_0_base import DataBase, QueueBase, NodePath
from typing import TypeVar, Type

Node = TypeVar('Node', bound=NodePath)


class DataOneToMany(DataBase[Node]):
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
        DataBase.__init__(self, type_queue=type_queue)
        self._goals_active = problem.goals

    @property
    def goals_active(self) -> set[Node]:
        """
        ========================================================================
         Return current Active-Goals (not found path to them yet).
        ========================================================================
        """
        return self._goals_active
