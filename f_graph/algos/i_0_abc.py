from f_core.processes.i_3_algo import Algorithm
from f_graph.path.problem import Problem
from f_graph.path.components.state import DataPath
from f_graph.path.components.ops import OpsPath
from f_graph.path.node import NodePath
from f_graph.path.components.path import PathBasic
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=Problem)
Node = TypeVar('Node', bound=NodePath)
Path = TypeVar('Path', bound=PathBasic)
Data = TypeVar('Data', bound=DataPath)
Ops = TypeVar('Ops', bound=OpsPath)


class AlgoPath(Generic[Problem, Path, Data, Ops],
               Algorithm[Problem, Path, Data, Ops]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 data: Data,
                 ops: Ops,
                 name: str = 'Path-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algorithm.__init__(self,
                           input=problem,
                           data=data,
                           ops=ops,
                           name=name)

    def run(self) -> Path:
        self._ops.generate(node=self._input.start)
        while not self._data.has_generated():
            best = self._data.pop_best_generated()
            if self._data.is_active_goal(node=best):
                self._data.remove_goal_active(goal=best)
                if not self._data.has_active_goals():
                    self._is_valid = True
                    return PathBasic()
                self._ops.explore(node=best)
