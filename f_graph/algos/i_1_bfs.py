from f_graph.algos.i_0_abc import AlgoPath
from f_graph.problems.i_1_path import ProblemPath
from f_graph.data.i_0_path import DataPath
from f_graph.ops.i_0_path import OpsPath
from f_graph.paths.path import PathBasic
from f_graph.nodes.i_1_path import NodePath
from f_ds.queues.i_1_fifo import QueueFIFO
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Path = TypeVar('Path', bound=PathBasic)
Data = TypeVar('Data', bound=DataPath)
Ops = TypeVar('Ops', bound=OpsPath)
Node = TypeVar('Node', bound=NodePath)


class BFS(Generic[Problem, Path, Data, Ops],
          AlgoPath[Problem, Path, Data, Ops]):
    """
    ============================================================================
     Breadth-First-Search Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 name: str = 'BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        data = DataPath(problem=problem, type_queue=QueueFIFO)
