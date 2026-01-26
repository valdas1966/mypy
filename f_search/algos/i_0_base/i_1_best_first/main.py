from f_search.ds.data import DataBestFirst
from abc import abstractmethod
from typing import Generic, TypeVar


Data = TypeVar('Data', bound=DataBestFirst)


class AlgoBestFirst(Generic[Data]):
    """
    ============================================================================
     1. Mixin for Best-First Algorithms.
     2. Concrete class must implement:
        ------------------------------------------------------------------------
          1. run() -> Solution
          2. _can_terminate() -> bool
          3. _need_relax(state) -> bool
          3. _relax(state) -> None
          4. _discover(state, parent) -> None
          5. _create_solution(is_valid: bool) -> Solution
    ============================================================================
    """

    @property
    def data(self) -> Data:
        """
        ========================================================================
         Get the Data.
        ========================================================================
        """
        return self._data

    def _should_continue(self) -> bool:
        """
        ========================================================================
         Return True if the Search should continue (if Frontier is not empty).
        ========================================================================
        """
        return bool(self._data.frontier)

    def _update_best(self) -> None:
        """
        ========================================================================
         Update the Best-State.
        ========================================================================
        """
        data = self._data
        data.best = data.frontier.pop()
    
    def _explore_best(self) -> None:
        """
        ========================================================================
         Explore the Best-State.
        ========================================================================
        """
        self._stats.explored += 1
        # Aliases
        data = self._data
        # Add State to Explored
        data.explored.add(data.best)
        # Get the Successors of the Best-State
        successors = self._problem.successors(state=data.best)
        # Operate Successors
        for succ in successors:
            # If the Successor is already explored, skip it
            if succ in data.explored:
                continue
            # If the Successor is not in the Frontier, discover it
            if succ not in data.frontier:
                self._discover(state=succ)
            # If the Successor is in the Frontier, relax it if needed
            else:   
                if self._need_relax(state=succ):
                    self._relax(state=succ)
