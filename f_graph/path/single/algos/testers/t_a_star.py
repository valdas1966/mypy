from f_graph.path.single.algos.a_star import AStar, Problem


def test_a_star():
    problem = Problem.gen_3x3()
    graph = problem.graph
    astar = AStar(problem=problem)
    solution = astar.run()
    assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                             graph[1, 2], graph[2, 2]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1],
                                       graph[0, 2], graph[1, 2]}
    assert set(solution.state.generated) == {graph[1, 0], graph[1, 1]}
    assert solution.state.best == problem.goal


def test_a_star_cache(problem):
    graph = problem.graph.clone()
    assert True


