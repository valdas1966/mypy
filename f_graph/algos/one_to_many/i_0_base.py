from f_graph.data.i_1_one_to_many import DataOneToMany, ProblemOneToMany
from f_graph.paths.i_1_one_to_many import PathOneToMany, NodePath
from f_graph.algos.path import AlgoPath, QueueBase
from typing import Type, TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToMany)
Node = TypeVar('Node', bound=NodePath)


class AlgoOneToMany(AlgoPath[Problem, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[QueueBase],
                 type_data: Type[DataOneToMany] = DataOneToMany,
                 type_path: Type[PathOneToMany] = PathOneToMany
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
         Search the shortest paths from Start to Goals.
        ========================================================================
        """
        self._generate_node(node=self.problem.start)
        while self._data.generated and not self.path:
            best = self._data.generated.pop()
            if best in self.data.goals_active:
                self.data.goals_active.remove(best)
                if not self.data.goals_active:
                    self.path.set_valid()
                    break
            self._explore_node(node=best)
