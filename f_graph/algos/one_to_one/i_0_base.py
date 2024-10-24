from f_graph.algos.i_0_path import AlgoPath, TypeData, TypeQueue
from f_graph.problems.i_2_one_to_one import ProblemOneToOne, NodePath
from f_graph.data.i_1_one_to_one import DataOneToOne
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Node = TypeVar('Node', bound=NodePath)


class AlgoOneToOne(AlgoPath[Problem, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: TypeQueue,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self,
                          problem=problem,
                          type_data=TypeData.ONE_TO_ONE,
                          type_queue=type_queue,
                          name=name)

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
        """
        ========================================================================
         Terminate the Search if the Best-Generated-Node is a Goal.
        ========================================================================
        """
        return best == self.problem.goal
