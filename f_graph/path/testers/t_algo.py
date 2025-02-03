from f_graph.path.generators.g_algo import GenAlgoPath, AlgoPath
from f_graph.path.problem import ProblemPath
from f_graph.path.solution import SolutionPath


def test() -> None:
    """
    ============================================================================
     Test problem attribute.
    ============================================================================
    """
    algo = GenAlgoPath.gen_3x3()
    assert isinstance(algo, AlgoPath)
    assert isinstance(algo.input, ProblemPath)
    assert isinstance(algo.run(), SolutionPath) 
