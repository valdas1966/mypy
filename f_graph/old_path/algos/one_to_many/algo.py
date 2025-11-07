from f_graph.old_path.algos.algo import AlgoPath
from f_graph.old_path.algos.one_to_one.algo import AlgoOneToOne, TypeAlgo
from f_graph.old_path.funcs.heuristic import Heuristic, TypeHeuristic
from f_graph.old_path.one_to_many.state import StateOneToMany as State, TypeQueue
from f_graph.old_path.one_to_many.problem import ProblemOneToMany as Problem
from f_graph.old_path.algos.one_to_one.solution import SolutionOneToOne, Node
from f_graph.old_path.core.solutions import SolutionsPath as Solutions


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
                 verbose: bool = False,
                 name: str = 'Algo One-To-Many') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoPath.__init__(self, problem=problem, name=name, verbose=verbose)
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
            if p.goal in sols:
                continue
            if self._is_shared:
                heuristic = Heuristic(graph=p.graph,
                                      goal=p.goal,
                                      type_heuristic=self._type_heuristic)
                self._state.update(heuristic=heuristic)
            if not self._is_shared:
                self._state = State(type_queue=self._type_queue)
            algo = AlgoOneToOne(problem=p,
                                state=self._state,
                                type_algo=self._type_algo,
                                is_shared=self._is_shared)
            sols[p.goal] = algo.run()
            for goal in self._problem.goals:
                if goal in self._state.explored:
                    if goal not in sols:
                        sols[goal] = SolutionOneToOne(goal=goal)
            if not sols[p.goal]:
                return Solutions(is_valid=False, sols=sols)
            # If the problem is shared, undo the pop of the goal node.
            # Because the goal was not explored, and he is relevant
            #  to be generated in the next search.
            if self._is_shared:
                self._state.generated.undo_pop(item=p.goal)
        return Solutions(is_valid=True, sols=sols)
