from f_graph.path.one_to_one.problem import ProblemOneToOne, Graph, Node
import pytest


@pytest.fixture
def graph_3x3() -> Graph:
    """
    ========================================================================
     Return a 3x3 test graph.
    ========================================================================
    """
    return Graph.gen_3x3()


@pytest.fixture 
def problem_3x3(graph_3x3: Graph) -> ProblemOneToOne:
    """
    ========================================================================
     Return a test problem with 3x3 graph.
    ========================================================================
    """
    start = graph_3x3[0, 0]
    goal = graph_3x3[2, 2]
    return ProblemOneToOne(graph=graph_3x3, start=start, goal=goal)


def test_start(problem_3x3: ProblemOneToOne) -> None:
    """
    ========================================================================
     Test that start node is correct.
    ========================================================================
    """
    assert problem_3x3.start == problem_3x3.graph[0, 0]


def test_goal(problem_3x3: ProblemOneToOne) -> None:
    """
    ========================================================================
     Test that goal node is correct. 
    ========================================================================
    """
    assert problem_3x3.goal == problem_3x3.graph[2, 2]


def test_clone(problem_3x3: ProblemOneToOne) -> None:
    """
    ========================================================================
     Test that clone creates an equal but separate problem.
    ========================================================================
    """
    clone = problem_3x3.clone()
    assert clone == problem_3x3
    assert clone is not problem_3x3


def test_reverse(problem_3x3: ProblemOneToOne) -> None:
    """
    ========================================================================
     Test that reverse swaps start and goal nodes.
    ========================================================================
    """
    reversed_problem = problem_3x3.reverse()
    assert reversed_problem.start == problem_3x3.goal
    assert reversed_problem.goal == problem_3x3.start


def test_gen_3x3() -> None:
    """
    ========================================================================
     Test the 3x3 problem generator.
    ========================================================================
    """
    problem = ProblemOneToOne.gen_3x3()
    assert problem.graph.nodes_count == 9
    assert problem.start == problem.graph[0, 0]
    assert problem.goal == problem.graph[2, 2]


def test_gen_4x4() -> None:
    """
    ========================================================================
     Test the 4x4 problem generator.
    ========================================================================
    """
    problem = ProblemOneToOne.gen_4x4()
    assert len(problem.graph.nodes()) == 16
    assert problem.start == problem.graph[0, 0]
    assert problem.goal == problem.graph[0, 3]
