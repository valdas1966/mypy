from f_graph.path.generators.gen_problem import GenProblem
from f_graph.path.nodes.i_1_cell import NodeCell
from f_graph.path.algos.bfs import BFS


def test_bfs():
    problem = GenProblem.one_goal_3x3(type_node=NodeCell)
    graph = problem.graph
    goal = graph[2, 2]
    bfs = BFS(problem=problem)
    path = bfs.run()
    assert path.get(goal=goal) == [graph[0, 0], graph[0, 1], graph[0, 2],
                                   graph[1, 2], graph[2, 2]]
    assert len(bfs._data._generated) == 0
    assert len(bfs._data._explored) == 8
