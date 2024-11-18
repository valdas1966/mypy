from f_graph.algos.i_0_abc import AlgoPath
from f_graph.path_finding.components.problem import Problem
from f_graph.path_finding.components.data import DataPath
from f_graph.path_finding.components.ops import OpsPath
from f_graph.path_finding.components.path import PathBasic
from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=Problem)
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
                 input: Problem,
                 data: Data,
                 ops: Ops,
                 name: str = 'BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self, input=input, data=data, ops=ops, name=name)
