from f_core.components.enum_callable import EnumCallable
from f_graph.path.algo import AlgoPath
from f_graph.path.one_to_one.algos.bfs import BFS
from f_graph.path.one_to_one.algos.a_star import AStar
from f_graph.path.one_to_many.state import StateOneToMany as State, TypeQueue
from f_graph.path.one_to_many.problem import ProblemOneToMany as Problem
from f_graph.path.one_to_many.solution import SolutionOneToMany as Solution


class TypeAlgo(EnumCallable):
    """
    ============================================================================
     Enum of Type-Algorithms.
    ============================================================================
    """
    BFS = BFS
    A_STAR = AStar


class AlgoOneToMany(AlgoPath[Problem, Solution]):
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
        if type_algo == TypeAlgo.BFS:
            self._type_queue = TypeQueue.FIFO
        self._state = state if state else State(type_queue=self._type_queue)
        self._is_shared = is_shared

    def run(self) -> Solution:
        """
        ========================================================================
         Run the One-To-Many Path-Finding Algorithm.
        ========================================================================
        """
        singles = self._problem.to_singles()
        for p in singles:
            if not self._is_shared:
                self._state = State(type_queue=self._type_queue)
            algo = self._type_algo(problem=p,
                                   state=self._state,
                                   is_shared=self._is_shared)
            sol = algo.run()

    