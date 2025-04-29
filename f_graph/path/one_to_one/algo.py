from f_graph.path.one_to_one.solution import SolutionOneToOne as Solution
from f_graph.path.one_to_one.problem import ProblemOneToOne as Problem
from f_graph.path.one_to_one.state import StateOneToOne as State, TypeQueue
from f_graph.path.one_to_one.flow import FlowOneToOne as Flow
from f_graph.path.one_to_one.ops import OpsOneToOne as Ops, TypeCounter
from f_graph.path.heuristic import Heuristic, TypeHeuristic
from f_graph.path.boundary import Boundary
from f_graph.path.stats import StatsPath
from f_graph.path.algo import AlgoPath
from f_graph.path.cache import Cache
from enum import Enum, auto


class TypeAlgo(Enum):
    """
    ============================================================================
     Enum of Type-Algorithms.
    ============================================================================
    """
    BFS = auto()
    A_STAR = auto()


class AlgoOneToOne(AlgoPath[Problem, Solution]):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_algo: TypeAlgo = TypeAlgo.A_STAR,
                 cache: Cache = None,
                 state: State = None,
                 boundary: Boundary = None,
                 is_shared: bool = False,
                 verbose: bool = False,
                 name: str = 'Path-Algorithm One-to-One') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        type_queue = TypeQueue.PRIORITY
        type_heuristic = TypeHeuristic.MANHATTAN
        if type_algo == TypeAlgo.BFS:
            type_queue = TypeQueue.FIFO
            type_heuristic = TypeHeuristic.ZERO
        problem = problem if is_shared else problem.clone()
        AlgoPath.__init__(self, problem=problem, verbose=verbose, name=name)
        self._cache = cache if cache else Cache()
        self._state = state if state else State(type_queue=type_queue)
        self._boundary = boundary if boundary else Boundary()
        self._heuristic = Heuristic(graph=problem.graph, goal=problem.goal,
                                    type_heuristic=type_heuristic)
        self._ops = Ops(problem=problem, cache=self._cache,
                        boundary=self._boundary, state=self._state,
                        heuristic=self._heuristic)

    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm to find the Optimal-Paths from Start to Goals.
        ========================================================================
        """
        self._run_pre()
        flow = self._create_flow()
        if not self._state.generated:
            flow.generate_start()
        while flow.should_continue():
            flow.select_best()
            if flow.is_path_found():
                self._run_post()
                return self._create_solution(is_found=True)
            flow.explore_best()
        self._run_post()
        return self._create_solution(is_found=False)

    def _create_flow(self) -> Flow:
        """
        ========================================================================
         Create a Flow object.
        ========================================================================
        """
        return Flow(problem=self._problem, state=self._state, ops=self._ops)

    def _create_solution(self, is_found: bool) -> Solution:
        """
        ========================================================================
         Create a Solution object.
        ========================================================================
        """
        stats = StatsPath(elapsed=self._elapsed,
                          generated=self._ops.counter[TypeCounter.GENERATED],
                          explored=self._ops.counter[TypeCounter.EXPLORED])
        return Solution(is_valid=is_found,
                        state=self._state,
                        cache=self._cache,
                        stats=stats)
