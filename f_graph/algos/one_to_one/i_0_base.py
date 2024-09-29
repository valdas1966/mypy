from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.data.i_1_one_to_one import DataOneToOne
from f_graph.paths.i_1_one_to_one import PathOneToOne
from f_graph.algos.path import AlgoPath, NodePath, QueueBase
from typing import Type, TypeVar

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
                 type_queue: Type[QueueBase],
                 type_data: Type[DataOneToOne] = DataOneToOne,
                 type_path: Type[PathOneToOne] = PathOneToOne
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self,
                          problem=problem,
                          type_data=type_data,
                          type_path=type_path,
                          type_queue=type_queue)

    def _search(self) -> None:
        """
        ========================================================================
         Search the shortest paths from Start to Goal.
        ========================================================================
        """
        self._generate_node(node=self.problem.start)
        while self._data.generated and not self.path:
            best = self._data.generated.pop()
            if best == self._problem.goal:
                self.path.set_valid()
                break
            self._explore_node(node=best)
