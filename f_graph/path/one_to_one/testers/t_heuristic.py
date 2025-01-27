from f_graph.path.one_to_one.generators.g_heuristic import GenHeuristic, Node
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne


def test_manhattan_distance():
    """
    ========================================================================
     Test that manhattan distance heuristic calculates correct distances.
    ========================================================================
    """
    # Setup
    problem = GenProblemOneToOne.gen_3x3()
    heuristic = GenHeuristic.gen_manhattan(problem=problem)

    # Test from origin
    actual = heuristic(node=problem.start)
    expected = 4  # Manhattan distance from (0,0) to (2,2) = |2-0| + |2-0| = 4
    assert actual == expected


def test_manhattan_zero_distance():
    """
    ========================================================================
     Test manhattan distance when node is at goal location.
    ========================================================================
    """
    # Setup
    problem = GenProblemOneToOne.gen_3x3()
    heuristic = GenHeuristic.gen_manhattan(problem=problem)

    # Test
    actual = heuristic(node=problem.goal)
    expected = 0
    assert actual == expected
