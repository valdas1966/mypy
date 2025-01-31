from f_graph.path.generators.g_heuristic import GenHeuristic
from f_graph.path.generators.g_graph import GenGraphPath


def test_manhattan_distance():
    """
    ========================================================================
     Test that manhattan distance heuristic calculates correct distances.
    ========================================================================
    """
    graph = GenGraphPath.gen_3x3()
    heuristic = GenHeuristic.gen_manhattan(graph=graph, goal=graph[2, 2])
    assert heuristic(node=graph[2, 2]) == 0
    assert heuristic(node=graph[0, 0]) == 4


def test_none() -> None:
    """
    ========================================================================
     Test that None-Heuristic returns None.
    ========================================================================
    """
    graph = GenGraphPath.gen_3x3()
    heuristic = GenHeuristic.gen_none()
    assert heuristic(node=graph[0, 0]) is None
