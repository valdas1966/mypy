from f_graph.data.i_2_one_to_many import DataOneToMany, ProblemOneToMany
from f_graph.algos.i_0_abc import AlgoPathABC, QueueBase, NodePath
from typing import Type, TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToMany)
Node = TypeVar('Node', bound=NodePath)


class AlgoOneToManyABC(AlgoPathABC[Problem, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[QueueBase]
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._data = type_data(problem=problem, type_queue=type_queue)
        AlgoPathABC.__init__(self, problem=problem, type_path=type_path)

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
