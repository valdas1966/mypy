from f_ai.hs.algos.one_to_one.a_star import (AStar, TerminationGoal,
                                             DataOneToOne, PathOneToOne)
from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_ai.hs.heuristics.i_1_manhattan import HeuristicsManhattan, NodeFCell


class UAlgosGrid:

    @staticmethod
    def astar(problem: ProblemOneToOne) -> AStar:
        heuristics = HeuristicsManhattan(distance=problem.graph.distance,
                                         goal=problem.goal)
        astar = AStar[ProblemOneToOne, TerminationGoal, DataOneToOne,
                      PathOneToOne, NodeFCell]
        return astar(problem=problem, heuristics=heuristics)
