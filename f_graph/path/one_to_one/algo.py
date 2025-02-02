from f_graph.path.stats import StatsPath
from f_graph.path.algo import AlgoPath, Node
from f_graph.path.one_to_one.problem import ProblemOneToOne as Problem
from f_graph.path.one_to_one.solution import SolutionOneToOne as Solution
from f_graph.path.one_to_one.state import State as State, Queue
from f_graph.path.one_to_one.ops import Ops as Ops
from f_graph.path.one_to_one.cache import Cache
from typing import Type, Callable


class AlgoOneToOne(AlgoPath[Problem, Solution]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    type_queue: Type[Queue] = Queue

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[Queue] = Queue,
                 cache: Cache = None,
                 heuristic: Callable[[Node], int] = None,
                 name: str = 'Path-Algorithm One-to-One') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self, problem=problem.clone(), name=name)
        self._cache = cache if cache else Cache()
        self._state = State(type_queue=type_queue)
        self._heuristic = heuristic
        self._ops = self._create_ops()

    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm to find the Optimal-Paths from Start to Goals.
        ========================================================================
        """
        self._run_pre()
        self._generate_start()
        while self._should_continue():
            self._select_best()
            if self._is_path_found():
                self._run_post()
                return self._create_solution(is_found=True)
            self._explore_best()
        self._run_post()
        return self._create_solution(is_found=False)

    def _create_ops(self) -> Ops:
        """
        ========================================================================
         Create an Ops object.
        ========================================================================
        """
        return Ops(problem=self._input,
                   state=self._state,
                   cache=self._cache,
                   heuristic=self._heuristic)

    def _create_solution(self, is_found: bool) -> Solution:
        """
        ========================================================================
         Create a Solution object.
        ========================================================================
        """
        stats = StatsPath(elapsed=self._elapsed,
                          explored=len(self._state.explored))
        return Solution(is_valid=is_found,
                        state=self._state,
                        cache=self._cache,
                        stats=stats)

    def _should_continue(self) -> bool:
        """
        ========================================================================
         Return True if the Algorithm should continue
          (optimal path for goals did not yet found and there are generated
          and not explored nodes).
        ========================================================================
        """
        return bool(self._state.generated)

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
        self._state.best = self._state.generated.pop()

    def _is_path_found(self) -> bool:
        """
        ========================================================================
         Return True if the Best-Generated Node is a Goal or in the Cache.
        ========================================================================
        """
        return (self._state.best == self._input.goal or
                self._state.best in self._cache)

    def _explore_best(self) -> None:
        """
        ========================================================================
         Explore the best generated node (generate its children).
        ========================================================================
        """
        self._ops.explore(node=self._state.best)

