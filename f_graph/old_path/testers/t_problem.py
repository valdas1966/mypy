from f_graph.old_path.generators.g_problem import GenProblemPath
from f_hs.ds.graphs.graph import GraphPath


def test_gen_3x3():
    """
    ============================================================================
     Test gen_3x3() method.
    ============================================================================
    """
    problem = GenProblemPath.gen_3x3()
    assert isinstance(problem.graph, GraphPath)
    