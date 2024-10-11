from f_graph.problems.i_2_one_to_one import ProblemOneToOne as ProblemOTO
from f_graph.graphs.u_1_grid import UGraphGrid, NodePathCell
from typing import Type


class UProblemOTO:
    """
    ============================================================================
     Utils for One-to-One Problem.
    ============================================================================
    """

    @staticmethod
    def generate(rows: int = 100,
                 pct_valid: int = 75,
                 type_node: Type[NodePathCell] = NodePathCell) -> ProblemOTO:
        """
        ========================================================================
         Generate a random One-to-One Problem (graph, start, goal).
        ========================================================================
        """
        graph = UGraphGrid.generate(rows=rows,
                                    pct_valid=pct_valid,
                                    type_node=type_node)
        start, goal = graph.sample(size=2)
        return ProblemOTO(graph=graph, start=start, goal=goal)