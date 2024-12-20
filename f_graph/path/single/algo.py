from f_graph.path.algo import AlgoPath, Node
from f_graph.path.single.data.problem import ProblemSingle as Problem
from f_graph.path.single.data.solution import SolutionSingle as Solution
from f_graph.path.single.components.state import State, Queue
from f_graph.path.single.components.ops import Ops
from typing import Type, Callable


class AlgoSingle(AlgoPath[Problem, Solution]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[Queue],
                 cache: set[Node] = None,
                 heuristic: Callable[[Node], int] = None,
                 name: str = 'Path-Algorithm-Single-Goal') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self,
                          problem=problem.clone(),
                          name=name)
        self._cache: dict[Node, Node] = {node: node for node in cache or set()}
        self._type_queue = type_queue
        self._heuristic = heuristic if heuristic else lambda _: 0
        self._state = self._create_state()
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
                return self._create_solution(is_path_found=True)
            self._explore_best()
        self._run_post()
        return self._create_solution(is_path_found=False)

    def _create_state(self) -> State[Node]:
        """
        ========================================================================
         Create a Data object.
        ========================================================================
        """
        return State[Node](type_queue=self._type_queue)

    def _create_ops(self) -> Ops[Node]:
        """
        ========================================================================
         Create an Ops object.
        ========================================================================
        """
        return Ops[Node](problem=self._input,
                         state=self._state,
                         cache=self._cache,
                         heuristic=self._heuristic)

    def _create_solution(self, is_path_found: bool) -> Solution:
        """
        ========================================================================
         Create a Solution object.
        ========================================================================
        """
        return Solution(state=self._state,
                        cache=self._cache,
                        elapsed=self.elapsed,
                        is_path_found=is_path_found)

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
