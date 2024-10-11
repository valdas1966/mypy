from f_ai.hs.algos.one_to_one.a_star import AStar
from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_ai.hs.heuristics.i_1_manhattan import HeuristicsManhattan, NodeFCell


class UAlgosGrid:

    @staticmethod
    def astar(problem: ProblemOneToOne) -> AStar:
        heuristics = HeuristicsManhattan(problem=problem).eval
        return AStar[ProblemOneToOne, NodeFCell](problem=problem,
                                                 heuristics=heuristics)
