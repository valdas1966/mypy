from f_graph.path.multi.problem import ProblemMulti, ProblemSingle, Graph


def test_goals():
    graph = Graph.gen_3x3()
    start = graph[0, 0]
    goals = [graph[1, 1], graph[1, 1]]
    problem = ProblemMulti(graph=graph, start=start, goals=goals)
    assert problem.goals == {graph[1, 1]}


def test_to_single():
    graph = Graph.gen_3x3()
    start = graph[0, 0]
    goals = [graph[1, 1], graph[2, 2]]
    problem = ProblemMulti(graph=graph, start=start, goals=goals)
    p_1 = ProblemSingle(graph=graph, start=start, goal=goals[0])
    p_2 = ProblemSingle(graph=graph, start=start, goal=goals[1])
    assert set(problem.to_singles()) == {p_1, p_2}
