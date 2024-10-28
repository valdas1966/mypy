from f_graph.algos.one_to_many.i_0_abc import (AlgoOneToManyABC, ProblemOneToMany,
                                               DataOneToMany, PathOneToMany,
                                               NodePath)
from f_ds.queues.i_1_fifo import QueueFIFO
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToMany)
Node = TypeVar('Node', bound=NodePath)


class BFS_OTM(AlgoOneToManyABC[Problem, Node]):
    """
    ============================================================================
     BFS-Algo fro One-to-Many Path Problems.
    ============================================================================
    """

    def __init__(self, problem: Problem) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToManyABC.__init__(self,
                                  problem=problem,
                                  type_queue=QueueFIFO,
                                  type_data=DataOneToMany,
                                  type_path=PathOneToMany)
