from f_graph.path.cache.algos.bfs import BFS
from f_graph.path.generators.gen_problem import GenProblem


problem = GenProblem.one_goal_3x3()
graph = problem.graph.copy()
goal = graph[2, 2]

bfs = BFS(problem=problem)
