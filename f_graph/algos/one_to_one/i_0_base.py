from f_graph.algos.i_0_path import AlgoPath, NodePath
from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Node = TypeVar('Node', bound=NodePath)


class AlgoOneToOne(AlgoPath[Problem, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """

    def _search(self) -> None:
        """
        ========================================================================
         Search the shortest paths from Start to Goal.
        ========================================================================
        """
        self._generate_node(node=self.problem.start)
        while self._data.generated and not self.path:
            best = self._data.generated.pop()
            if self._can_terminate(best=best):
                self.path.set_valid()
                break
            self._explore_node(node=best)

    def _can_terminate(self, best: Node) -> bool:
        return best == self.problem.goal
