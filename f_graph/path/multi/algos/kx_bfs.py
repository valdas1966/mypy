from f_graph.path.multi.algo import AlgoMulti, ProblemMulti, SolutionMulti
from f_graph.path.multi.statemulti import StateMulti
from f_graph.path.single.algos.bfs import BFS, Node


class KX_BFS(AlgoMulti):

    def __init__(self,
                 problem: ProblemMulti,
                 name: str = 'KX BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoMulti.__init__(self, problem=problem, name=name)

    def run(self) -> SolutionMulti:
        paths: dict[Node, list[Node]] = dict()
        elapsed = 0
        state = StateMulti()
        problems = self._input.to_singles()
        for problem in problems:
            bfs = BFS(problem=problem)
            sol_single = bfs.run()
            if not sol_single:
                return SolutionMulti(is_valid=False,
                                     elapsed=elapsed,
                                     state=state,
                                     paths=paths)
            state.add_generated(list(sol_single.state.generated))
            state.add_explored(sol_single.state.explored)
            elapsed += sol_single.elapsed
            paths[problem.goal] = sol_single.path
        return SolutionMulti(is_valid=True,
                             elapsed=elapsed,
                             state=state,
                             paths=paths)
