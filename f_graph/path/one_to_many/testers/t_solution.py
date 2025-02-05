from f_graph.path.one_to_many.generators.g_solution import GenSolutionOneToMany


def test_solution_one_to_many():
    """
    ========================================================================
     Test SolutionOneToMany.
    ========================================================================
    """
    solution = GenSolutionOneToMany.gen_3x3()
    assert solution
    assert len(solution.paths) == 3
    assert len(solution.stats) == 3
    assert solution.elapsed == 30
    assert solution.generated == 60
    assert solution.explored == 90
