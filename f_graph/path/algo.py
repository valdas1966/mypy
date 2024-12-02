from f_cs.algo import Algo
from f_graph.path.config import (Path, Data, Ops, TQueue,
                                 TProblem, TPath, TData, TOps, TNode)
from typing import Generic, Type


class AlgoPath(Generic[TProblem, TPath, TData, TOps, TNode],
               Algo[TProblem, TPath]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: TProblem,
                 type_queue: Type[TQueue],
                 name: str = 'Path-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoABC.__init__(self,
                         _input=problem.clone(),
                         name=name)
        self._type_queue = type_queue
        self._data = self._create_data()
        self._ops = self._create_ops()
        self._path = self._create_path()
        self._best = None

    def run(self) -> Path:
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
                    return self._path
            self._explore_best()

    def _create_data(self) -> Data:
        """
        ========================================================================
         Create a Data object.
        ========================================================================
        """
        return Data[TNode](problem=self._input, type_queue=self._type_queue)

    def _create_ops(self) -> Ops:
        """
        ========================================================================
         Create an Ops object.
        ========================================================================
        """
        return Ops[TNode](problem=self._input, data=self._data)

    def _create_path(self) -> Path:
        """
        ========================================================================
         Create a Path object.
        ========================================================================
        """
        return Path[TNode](problem=self._input)

    def _should_continue(self) -> bool:
        """
        ========================================================================
         Return True if the Algorithm should continue
          (optimal path for goals did not yet found and there are generated
          and not explored nodes).
        ========================================================================
        """
        return self._data.has_generated()

    def _should_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Algorithm should terminate
          (optimal path to goal were found).
        ========================================================================
        """
        return not self._data.has_active_goals()

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
        self._best = self._data.pop_generated()

    def _is_path_found(self) -> bool:
        """
        ========================================================================
         Return True if the Best-Generated Node is a Goal.
        ========================================================================
        """
        return self._best_is_goal()

    def _on_path_found(self) -> None:
        self._data.remove_active_goal(goal=self._best)
        self._path.construct(goal=self._best)

    def _best_is_goal(self) -> bool:
        """
        ========================================================================
         Return True if the best generated node is an Active-Goal.
        ========================================================================
        """
        return self._data.is_active_goal(node=self._best)

    def _explore_best(self) -> None:
        """
        ========================================================================
         Explore the best generated node (generate its children).
        ========================================================================
        """
        self._ops.explore(node=self._best)
