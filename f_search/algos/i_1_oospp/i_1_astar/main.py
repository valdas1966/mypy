from f_search.algos.i_1_oospp.i_0_base import AlgoOOSPP
from f_search.problems import ProblemOOSPP, State
from f_search.solutions import SolutionOOSPP
from f_search.ds.generated import Generated
from f_search.stats import StatsOOSPP
from f_search.ds.cost import Cost
from f_search.ds.path import Path


class AStar(AlgoOOSPP):
    """
    ============================================================================
     A* Algorithm for One-to-One Shortest-Path-Problem.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemOOSPP,
                 verbose: bool = False,
                 name: str = 'AStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOOSPP.__init__(self,
                           problem=problem,
                           verbose=verbose,
                           name=name)

    def _run_pre(self,
                 generated: Generated | None = None,
                 explored: set[State] | None = None) -> None:
        """
        ========================================================================
         Init data structures.
        ========================================================================
        """
        AlgoOOSPP._run_pre(self)
        self._generated = generated if generated else Generated()
        self._explored = explored if explored else set()
        self._counters['GENERATED'] = 0
        self._counters['UPDATED'] = 0
        self._counters['EXPLORED'] = 0

    def run(self,
            generated: Generated | None = None,
            explored: set[State] | None = None) -> SolutionOOSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._run_pre(generated=generated, explored=explored)
        self._generate(state=self._problem.start)
        while self._generated:
            self._best = self._generated.pop()
            if self._can_terminate():
                return self._create_solution(is_valid=True)
            self._explore()
        return self._create_solution(is_valid=False)

    def _explore(self) -> None:
        """
        ========================================================================
         Explore the Best-State.
        ========================================================================
        """
        # Increment explored counter
        self._counters['EXPLORED'] += 1
        # Add State to Explored
        self._explored.add(self._best)
        # Generate State's unexplored Successors
        successors = self._problem.successors(state=self._best)
        for succ in successors:
            if succ not in self._explored:
                self._generate(state=succ)

    def _generate(self, state: State) -> None:
        """
        ========================================================================
         Generate a new state.
        ========================================================================
        """
        # New State (not in Generated)
        if state not in self._generated:
            self._counters['GENERATED'] += 1
            self._update_cost(state=state)
            self._generated.push(state=state, cost=self._cost[state])
        # If Best is a better parent for a given State
        elif self._best:
            if self._g[state] > self._g[self._best] + 1:
                self._counters['UPDATED'] += 1
                self._update_cost(state=state)
                self._generated.push(state=state, cost=self._cost[state])

    def _heuristic(self, state: State) -> int:
        """
        ========================================================================
         Return the Heuristic-Value of the given State 
          (Manhattan-Distance to the Goal).
        ========================================================================
        """
        cell_state = state.key
        cell_goal = self._problem.goal.key
        return cell_state.distance(other=cell_goal)

    def _update_cost(self, state: State) -> None:
        """
        ========================================================================
         Update the Cost of the given State.
        ========================================================================
        """
        self._parent[state] = self._best
        self._g[state] = self._g[self._best] + 1 if self._best else 0
        self._h[state] = self._heuristic(state=state)
        self._cost[state] = Cost(key=state,
                                 g=self._g[state],
                                 h=self._h[state])

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-State in Generated-List.
        ========================================================================
        """
        return self._best == self._problem.goal

    def _reconstruct_path(self) -> Path:
        """
        ========================================================================
         Reconstruct the Path from Start to Goal.
        ========================================================================
        """
        states = list[State]()
        state = self._best
        while state:
            states.append(state)
            state = self._parent[state]
        states = states[::-1]
        return Path(states=states)

    def _run_post(self) -> None:
        """
        ========================================================================
         Run necessary operations after the end of the Algorithm.
        ========================================================================
        """
        AlgoOOSPP._run_post(self)
        self._stats = self._calc_stats()

    def _calc_stats(self) -> StatsOOSPP:
        """
        ========================================================================
         Calculate the Stats.
        ========================================================================
        """
        return StatsOOSPP(elapsed=self.elapsed,
                          generated=self._counters['GENERATED'],
                          updated=self._counters['UPDATED'],
                          explored=self._counters['EXPLORED'])

    def _create_solution(self, is_valid: bool) -> SolutionOOSPP:
        """
        ========================================================================
         Create the Solution.
        ========================================================================
        """
        self._run_post()
        if is_valid:
            path = self._reconstruct_path()
            return SolutionOOSPP(is_valid=True,
                                 path=path,
                                 stats=self._stats)
        else:
            return SolutionOOSPP(is_valid=False,
                                 path=None,
                                 stats=self._stats)
