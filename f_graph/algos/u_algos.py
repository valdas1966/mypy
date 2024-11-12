from f_graph.algos.i_0_abc import AlgoPath
from f_graph.path_finding.problem import Problem
from f_graph.path_finding.data import DataPath
from f_graph.path_finding.ops import OpsPath
from f_graph.path_finding.path import PathBasic
from f_graph.nodes.i_1_path import NodePath
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
