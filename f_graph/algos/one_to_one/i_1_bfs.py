from f_graph.algos.one_to_one.i_0_base import (AlgoOneToOne, ProblemOneToOne,
                                               TerminationGoal, DataOneToOne,
                                               PathOneToOne, NodePath)
from f_ds.queues.i_1_fifo import QueueFIFO
from typing import TypeVar, Type

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Termination = TypeVar('Termination', bound=TerminationGoal)
Data = TypeVar('Data', bound=DataOneToOne)
Path = TypeVar('Path', bound=PathOneToOne)
Node = TypeVar('Node', bound=NodePath)


class BFS(AlgoOneToOne[Problem, Node]):
    """
    ============================================================================
     Breadth-First-Search Algorithm.
    ============================================================================
    """

    def __init__(self, problem: Problem,
                 type_termination: Type[TerminationGoal] = TerminationGoal) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              type_queue=QueueFIFO,
                              type_termination=type_termination)
