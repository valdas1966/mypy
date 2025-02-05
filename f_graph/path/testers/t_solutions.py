from f_graph.path.generators.g_solutions import GenSolutionsPath


def test_solutions() -> None:
    """
    ========================================================================
     Test the Solutions class.
    ========================================================================
    """
    sols = GenSolutionsPath.gen_30_60_90()
    assert len(sols) == 3
    assert sols.elapsed == 30
    assert sols.generated == 60
    assert sols.explored == 90

