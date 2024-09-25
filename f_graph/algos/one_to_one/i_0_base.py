from f_graph.problems.i_2_one_to_one import ProblemOneToOne, NodePath
from f_graph.data.i_1_one_to_one import DataOneToOne
from f_graph.algos.path import AlgoPath
from typing import TypeVar

Node = TypeVar('Node', bound=NodePath)
Problem = TypeVar('Problem', bound=ProblemOneToOne)
Data = TypeVar('Data', bound=DataOneToOne)


class AlgoOneToOne(AlgoPath[Node, Problem, Data]):
    """
    ============================================================================
     Base-Algorithm for One-To-One path problems.
    ============================================================================
    """

    def _search(self) -> None:
        """
        ========================================================================
         Search the shortest path from Start to Goal.
        ========================================================================
        """
        self._generate_node(node=self.problem.start)
        while self._data.generated and not self._is_found:
            best = self._data.generated.pop()
            if best == self._problem.goal:
                self._is_found = True
                break
            self._explore_node(node=best)
