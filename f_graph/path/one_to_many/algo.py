from f_graph.path.algo import AlgoPath
from f_graph.path.heuristic import Heuristic, TypeHeuristic
from f_graph.path.one_to_many.state import StateOneToMany as State, TypeQueue
from f_graph.path.one_to_many.problem import ProblemOneToMany as Problem
from f_graph.path.one_to_one.solution import SolutionOneToOne, Node
from f_graph.path.solutions import SolutionsPath as Solutions


class AlgoOneToMany(AlgoPath[Problem, Solutions]):
    """
    ============================================================================
     One-To-Many Path-Finding Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 state: State = None,
                 type_algo: TypeAlgo = TypeAlgo.A_STAR,
                 is_shared: bool = True,
                 name: str = 'Algo One-To-Many') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self, problem=problem, name=name)
        self._type_algo = type_algo
        self._type_queue = TypeQueue.PRIORITY
        self._type_heuristic = TypeHeuristic.MANHATTAN
        if type_algo == TypeAlgo.BFS:
            self._type_queue = TypeQueue.FIFO
            self._type_heuristic = TypeHeuristic.ZERO
        self._state = state if state else State(type_queue=self._type_queue)
        self._is_shared = is_shared

    def run(self) -> Solutions:
        """
        ========================================================================
         Run the One-To-Many Path-Finding Algorithm.
        ========================================================================
        """
        sols: dict[Node, SolutionOneToOne] = dict()
        singles = self._problem.to_singles()
        for p in singles:
            if self._is_shared:
                heuristic = Heuristic(graph=p.graph,
                                      goal=p.goal,
                                      type_heuristic=self._type_heuristic)
                self._state.update(heuristic=heuristic)
            if not self._is_shared:
                self._state = State(type_queue=self._type_queue)
            algo = self._type_algo(problem=p,
                                   state=self._state,
                                   is_shared=self._is_shared)
            sols[p.goal] = algo.run()
            if not sols[p.goal]:
                return Solutions(is_valid=False, sols=sols)
            self._state.generated.undo_pop(item=p.goal)
        return Solutions(is_valid=True, sols=sols)
