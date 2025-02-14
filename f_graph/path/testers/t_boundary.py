from f_graph.path.generators.g_boundary import GenBoundary, GenGraphPath


def test_3x3() -> None:
    """
    ========================================================================
     Test the Boundary for a 3x3 Grid.
    ========================================================================
    """
    boundary = GenBoundary.gen_3x3()
    graph = GenGraphPath.gen_3x3()
    assert boundary[graph[1, 0]]() == 1
    assert boundary[graph[1, 1]]() == 0
    assert boundary[graph[1, 2]]() == -1
    assert boundary[graph[2, 0]]() == 0
