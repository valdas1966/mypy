from f_graph.old_path.generators.g_boundary import GenBoundary, GenGraphPath


def test_first_row_branch_3x3() -> None:
    """
    ========================================================================
     Test the Boundary for a 3x3 Grid.
    ========================================================================
    """
    boundary = GenBoundary.first_row_branch_3x3()
    graph = GenGraphPath.gen_3x3()
    assert boundary[graph[1, 0]] == 1
    assert boundary[graph[1, 1]] == 0
    assert boundary[graph[1, 2]] == -1
