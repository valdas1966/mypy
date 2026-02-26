from f_search.ds.state import StateBase
from typing import TypeVar, Callable, Generic

State = TypeVar('State', bound=StateBase)


class Propagation(Generic[State]):
    """
    ========================================================================
     Multi-source Wavefront Expansion with Decaying Values.
    ========================================================================
     Propagates integer values outward from source states on a graph.
     At each step, values decrease by 1 (triangle inequality).
     States in the excluded set are skipped (already have known values).
     Optionally prunes states whose propagated value is not tighter than
      a given threshold function (e.g., a heuristic).
    ========================================================================
     Intuition:
    ------------------------------------------------------------------------
     Imagine dropping stones into a pond at multiple points. Each stone
      creates a ripple that spreads outward, losing energy (value) with
      each step. Where ripples from different stones overlap, the
      strongest ripple (highest value) wins. Ripples that are too weak
      (below a known threshold) are ignored.
    ========================================================================
     Use Cases:
    ------------------------------------------------------------------------
     1. Propagating lower bounds from explored states to their neighbors
        after a search (e.g., A* bounds propagation).
     2. Spreading heuristic estimates outward from known states.
     3. Any scenario where decaying information spreads on a graph from
        multiple source points.
    ========================================================================
     Example:
    ------------------------------------------------------------------------
     Given a linear graph: A - B - C - D - E

     sources = {A: 6}, excluded = {A}, depth=3

     Step 1: A->B with value 5
     Step 2: B->C with value 4
     Step 3: C->D with value 3

     Returns: {B: 5, C: 4, D: 3}
    ========================================================================
     Example with pruning (prune returns h-value for each state):
    ------------------------------------------------------------------------
     sources = {A: 6}, excluded = {A}, depth=3,
      prune(B)=2, prune(C)=5

     Step 1: A->B with value 5 > prune(B)=2 -> kept
     Step 2: B->C with value 4 <= prune(C)=5 -> pruned (and subtree)

     Returns: {B: 5}
    ========================================================================
     Example with multiple sources (max value wins):
    ------------------------------------------------------------------------
     Given: A - X - B

     sources = {A: 4, B: 6}, excluded = {A, B}, depth=1

     Step 1: A->X with value 3, B->X with value 5 -> max wins

     Returns: {X: 5}
    ========================================================================
    """

    Factory: type = None

    def __init__(self,
                 sources: dict[State, int],
                 excluded: set[State],
                 successors: Callable[[State], list[State]],
                 depth: int,
                 prune: Callable[[State], int] | None = None
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self._sources = sources
        self._excluded = excluded
        self._successors = successors
        self._depth = depth
        self._prune = prune

    def run(self) -> dict[State, int]:
        """
        ====================================================================
         Run the Propagation and return the Result.
        ====================================================================
        """
        frontier = dict(self._sources)
        result: dict[State, int] = {}
        for _ in range(self._depth):
            # Expand the current wavefront level Frontier
            frontier = self._expand(frontier=frontier)
            # If there is no propagation potential, stop
            if not frontier:
                break
            # Update the result with the new frontier
            result.update(frontier)
            # Update excluded (already propagated)
            self._excluded.update(frontier.keys())
        return result

    def _expand(self,
                frontier: dict[State, int]
                ) -> dict[State, int]:
        """
        ====================================================================
         Expand one wavefront level from all frontier states.
        ====================================================================
        """
        next_frontier: dict[State, int] = {}
        for state, value in frontier.items():
            # IF there is a propagation potential
            if value > 1:
                self._expand_state(state=state,
                                   value=value,
                                   next_frontier=next_frontier)
        return next_frontier

    def _expand_state(self,
                      state: State,
                      value: int,
                      next_frontier: dict[State, int]
                      ) -> None:
        """
        ====================================================================
         Expand a single state: propagate its value to valid
          successors (by decreasing the value by 1).
        ====================================================================
        """
        for succ in self._successors(state):
            if succ in self._excluded:
                continue
            value_propagated = value - 1
            # Skip if pruning threshold provides a tighter value
            if (self._prune
                    and value_propagated <= self._prune(state=succ)):
                continue
            # Keep the max value if multiple sources reach same state
            if value_propagated > next_frontier.get(succ, -1):
                next_frontier[succ] = value_propagated
