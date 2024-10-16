from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.data.i_2_one_to_one import DataOneToOne
from f_graph.paths.i_1_one_to_one import PathOneToOne
from f_graph.algos.path import AlgoPath, NodePath
from f_graph.termination.one_to_one.i_0_goal import TerminationGoal
from f_graph.termination.one_to_one.i_1_cache import TerminationCache
from f_ds.queues.i_0_base import QueueBase
from typing import Type, TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Termination = TypeVar('Termination', bound=TerminationGoal)
Data = TypeVar('Data', bound=DataOneToOne)
Path = TypeVar('Path', bound=PathOneToOne)
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
                 type_termination: Type[TerminationGoal] = TerminationGoal,
                 type_data: Type[DataOneToOne] = DataOneToOne,
                 type_path: Type[PathOneToOne] = PathOneToOne
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._type_queue = type_queue
        self._type_termination = type_termination
        self._type_data = type_data
        self._type_path = type_path
        AlgoPath.__init__(self, problem=problem)

    def _create_termination(self) -> Termination:
        """
        ========================================================================
         Create a Termination Exam (on Search reaches the Goal).
        ========================================================================
        """
        if issubclass(self._type_termination, TerminationCache):
            return self._type_termination(goal=self.problem.goal,
                                          cache=self.data.cache)
        return self._type_termination(goal=self.problem.goal)

    def _create_data(self) -> Data:
        """
        ========================================================================
         Create a Data for Algorithm (Generated and Explored).
        ========================================================================
        """
        return self._type_data(type_queue=self._type_queue)

    def _create_path(self) -> Path:
        """
        ========================================================================
         Create a Path for Algorithm (Validity and Path from Start to Goal).
        ========================================================================
        """
        return self._type_path(goal=self.problem.goal)

    def _search(self) -> None:
        """
        ========================================================================
         Search the shortest paths from Start to Goal.
        ========================================================================
        """
        self._generate_node(node=self.problem.start)
        while self._data.generated and not self.path:
            best = self._data.generated.pop()
            if self.termination.can(node=best):
                self.path.set_valid()
                break
            self._explore_node(node=best)
