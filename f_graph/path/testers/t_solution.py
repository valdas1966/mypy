from f_graph.path.generators.g_solution import GenSolutionPath


def test_is_valid() -> None:
    """
    ============================================================================
     Test is_valid attribute.
    ============================================================================
    """
    solution = GenSolutionPath.gen_3x3()
    assert solution


def test_stats() -> None:
    """
    ============================================================================
     Test stats attribute.
    ============================================================================
    """
    solution = GenSolutionPath.gen_3x3()
    assert solution.stats.elapsed == 10
    assert solution.stats.explored == 20
