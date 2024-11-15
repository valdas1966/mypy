from f_cs.algo import Algorithm
from f_graph.path_finding.protocols.problem import Problem
from f_graph.path_finding.protocols.data import Data
from f_graph.path_finding.protocols.ops import Ops
from f_graph.path_finding.protocols.path import Path


class AlgoPath(Algorithm[Problem, Path, Data, Ops]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 data: Data,
                 ops: Ops,
                 path: Path,
                 name: str = 'Path-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algorithm.__init__(self,
                           _input=problem,
                           data=data,
                           ops=ops,
                           name=name)
        self._path = path
        self._best = None

    def run(self) -> Path:
        """
        ========================================================================
         Run the Algorithm to find the Optimal-Paths from Start to Goals.
        ========================================================================
        """
        self._generate_start()
        while self._should_continue():
            self._select_best()
            if self._best_is_goal():
                self._handle_goal()
                if self._should_terminate():
                    return self._path
            self._explore_best()

    def _should_continue(self) -> bool:
        """
        ========================================================================
         Return True if the Algorithm should continue
          (optimal path for goals did not yet found and there are generated
          and not explored nodes).
        ========================================================================
        """
        return self._data.has_generated()

    def _should_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Algorithm should terminate
          (optimal path to goal were found).
        ========================================================================
        """
        return self._data.has_active_goals()

    def _generate_start(self) -> None:
        """
        ========================================================================
         Generate a Start node.
        ========================================================================
        """
        self._ops.generate(node=self._input.start)

    def _select_best(self) -> None:
        """
        ========================================================================
         Select a best node from the generated queue.
        ========================================================================
        """
        self._best = self._data.pop_generated()

    def _best_is_goal(self) -> bool:
        """
        ========================================================================
         Return True if the best generated node is an Active-Goal.
        ========================================================================
        """
        return self._data.is_active_goal(node=self._best)

    def _handle_goal(self) -> None:
        """
        ========================================================================
         Remove a Goal from an Active-Goals (optimal path was found).
        ========================================================================
        """
        self._data.remove_active_goal(goal=self._best)

    def _explore_best(self) -> None:
        """
        ========================================================================
         Explore the best generated node (generate its children).
        ========================================================================
        """
        self._ops.explore(node=self._best)
