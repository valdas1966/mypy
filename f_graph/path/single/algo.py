from f_graph.algo import AlgoGraph
from f_graph.path.single.components.problem import ProblemPath as Problem
from f_graph.path.single.components.solution import Solution
from f_graph.path.single.components.state import State, Queue
from f_graph.path.single.components.ops import Ops
from f_graph.path.node import NodePath as Node
from typing import Type


class AlgoPath(AlgoGraph[Problem, Solution]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[Queue],
                 cache: set[Node] = None,
                 name: str = 'Path-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoGraph.__init__(self,
                           _input=problem.clone(),
                           name=name)
        self._cache = cache or set()
        self._type_queue = type_queue
        self._state = self._create_state()
        self._ops = self._create_ops()
        self._solution = self._create_solution()

    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm to find the Optimal-Paths from Start to Goals.
        ========================================================================
        """
        self._generate_start()
        while self._should_continue():
            self._select_best()
            if self._is_path_found():
                self._on_path_found()
                if self._should_terminate():
                    return self._solution
            self._explore_best()

    def _create_state(self) -> State[Node]:
        """
        ========================================================================
         Create a Data object.
        ========================================================================
        """
        return State[Node](problem=self._input, type_queue=self._type_queue)

    def _create_ops(self) -> Ops[Node]:
        """
        ========================================================================
         Create an Ops object.
        ========================================================================
        """
        return Ops[Node](problem=self._input, data=self._state)

    def _create_solution(self) -> Solution[Node]:
        """
        ========================================================================
         Create a Path object.
        ========================================================================
        """
        return Solution[Node](problem=self._input)

    def _should_continue(self) -> bool:
        """
        ========================================================================
         Return True if the Algorithm should continue
          (optimal path for goals did not yet found and there are generated
          and not explored nodes).
        ========================================================================
        """
        return self._state.has_generated()

    def _should_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Algorithm should terminate
          (optimal path to goal were found).
        ========================================================================
        """
        return not self._state.has_active_goals()

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
        self._state.set_best()

    def _is_path_found(self) -> bool:
        """
        ========================================================================
         Return True if the Best-Generated Node is a Goal.
        ========================================================================
        """
        return self._best_is_goal() or self._best in self._cache

    def _on_path_found(self) -> None:
        """
        ========================================================================
         Remove Active-Goal and construct an Optimal-Path to it.
        ========================================================================
        """
        self._state.remove_active_goal(goal=self._best)
        self._solution.construct(goal=self._best)

    def _best_is_goal(self) -> bool:
        """
        ========================================================================
         Return True if the best generated node is an Active-Goal.
        ========================================================================
        """
        return self._state.is_active_goal(node=self._best)

    def _explore_best(self) -> None:
        """
        ========================================================================
         Explore the best generated node (generate its children).
        ========================================================================
        """
        self._ops.explore(node=self._best)
