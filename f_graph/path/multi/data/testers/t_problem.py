from f_graph.path.multi.data.problem import ProblemMulti, Graph


def test_goals():
    graph = Graph.gen_3x3()
    start = graph[0, 0]
    goals = [graph[1, 1], graph[1, 1]]
    problem = ProblemMulti(graph=graph, start=start, goals=goals)
    assert problem.goals == {graph[1, 1]}
