from f_graph.problems.i_2_one_to_many import ProblemOneToMany, NodePath
from f_graph.data.i_0_one_to_one import DataOneToOne
from f_ds.queues.i_0_base import QueueBase
from typing import Type, TypeVar

Node = TypeVar('Node', bound=NodePath)


class DataOneToMany(DataOneToOne[Node]):
    """
    ============================================================================
     Data for One-To-Many Search-Algorithm.
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
        DataOneToOne.__init__(self, type_queue=type_queue)
        self._goals_active = problem.goals

    @property
    def goals_active(self) -> set[Node]:
        """
        ========================================================================
         Return current Active-Goals (not found path to them yet).
        ========================================================================
        """
        return self._goals_active
