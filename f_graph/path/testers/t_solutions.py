from f_graph.path.generators.g_solutions import GenSolutionsPath


def test_solutions() -> None:
    sols = GenSolutionsPath.gen_30_60_90()
    assert sols.elapsed == 30
    assert sols.generated == 60
    assert sols.explored == 90

