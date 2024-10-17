from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.data.i_1_one_to_one import DataOneToOne
from f_graph.paths.i_1_one_to_one import PathOneToOne
from f_graph.algos.i_1_cache import AlgoCache, NodePath
from f_graph.termination.one_to_one.i_1_cache import TerminationCache
from f_ds.queues.i_0_base import QueueBase
from typing import Type, TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Termination = TypeVar('Termination', bound=TerminationCache)
Data = TypeVar('Data', bound=DataOneToOne)
Path = TypeVar('Path', bound=PathOneToOne)
Node = TypeVar('Node', bound=NodePath)


class AlgoOneToOne(AlgoCache[Problem, Node]):
    """
    ============================================================================
     Base-Algorithm for One-To-One paths problems.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[QueueBase],
                 type_termination: Type[TerminationCache] = TerminationCache,
                 type_data: Type[DataOneToOne] = DataOneToOne,
                 type_path: Type[PathOneToOne] = PathOneToOne,
                 cache: set[Node] = None
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
        AlgoCache.__init__(self, problem=problem, cache=cache)

    def _create_termination(self) -> Termination:
        """
        ========================================================================
         Create a Termination Exam (on Search reaches the Goal).
        ========================================================================
        """
        return self._type_termination(goal=self.problem.goal,
                                      cache=self.cache)

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
