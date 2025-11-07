from f_graph.old_path.algos.fore_and_back.algo import AlgoForeAndBack
from f_graph.old_path.algos.one_to_many.generators.g_problem import GenProblemOneToMany


def test_algo_fore_and_back():
    """
    ========================================================================
    
    ========================================================================
    """
    problem = GenProblemOneToMany.corner_3_goals()
    algo = AlgoForeAndBack(problem=problem, depth_boundary=1)
    sols = algo.run()
    assert sols
    graph = problem.graph
    goal_13 = graph[1, 3]
    goal_02 = graph[0, 2]
    goal_03 = graph[0, 3]
    assert sols.stats[goal_13].explored == 8
    assert sols.stats[goal_02].explored == 1
    assert sols.stats[goal_03].explored == 4
    assert sols.explored == 13


