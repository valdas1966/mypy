from f_graph.algos.i_0_abc import AlgoPath
from f_graph.path.single.components.problem import Problem
from f_graph.path.single.components.state import DataPath
from f_graph.path.single.components.ops import OpsPath
from f_graph.path.single.components.solution import PathBasic
from f_graph.path.node import NodePath
from f_ds.queues.i_1_fifo import QueueFIFO
from typing import TypeVar

Problem = TypeVar('Problem', bound=Problem)
Path = TypeVar('Path', bound=PathBasic)
Data = TypeVar('Data', bound=DataPath)
Ops = TypeVar('Ops', bound=OpsPath)
Node = TypeVar('Node', bound=NodePath)


class UAlgos:
    """
    ============================================================================
     Path-Algorithms Generator.
    ============================================================================
    """

    @staticmethod
    def bfs(problem: Problem, name: str = 'BFS') -> AlgoPath:
        path = PathBasic()
        data = DataPath(problem=problem, type_queue=QueueFIFO)
        ops = OpsPath(problem=problem, data=data)
        return AlgoPath(problem=problem, data=data, ops=ops, name=name)
