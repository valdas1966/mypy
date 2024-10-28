from f_graph.problems.i_2_one_to_many import ProblemOneToMany
from f_graph.data.i_1_one_to_one import DataOneToOne, Node, Queue
from typing import Type


class DataOneToMany(DataOneToOne[Node]):
    """
    ============================================================================
     Class of Data for One-to-Many Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOneToMany,
                 type_queue: Type[Queue],
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        DataOneToOne.__init__(self, type_queue=type_queue)
        self._goals_active = problem.goals

    @property
    def goals_active(self) -> set[Node]:
        """
        ========================================================================
         Return current Active-Goals (not found paths to them yet).
        ========================================================================
        """
        return self._goals_active
