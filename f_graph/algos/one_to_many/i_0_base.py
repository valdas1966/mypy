from f_graph.data.i_2_one_to_many import DataOneToMany, ProblemOneToMany
from f_graph.paths.i_1_one_to_many import PathOneToMany, NodePath
from f_graph.algos.i_0_path import AlgoPath, QueueBase
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
        self._data = type_data(problem=problem, type_queue=type_queue)
        AlgoPath.__init__(self, problem=problem, type_path=type_path)

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
                self._on_goal_found(goal=best)
                if not self.data.goals_active:
                    self.path.set_valid()
                    break
            self._explore_node(node=best)

    def _on_goal_found(self, goal: Node) -> None:
        """
        ========================================================================
         Do when Path to one of the Goals is found.
        ========================================================================
        """
        self.data.goals_active.remove(goal)
