from f_graph.path_finding.algos.bfs import BFS
from f_graph.path_finding.generators.gen_problem import GenProblem


problem = GenProblem.one_goal_3x3()
print(problem)
bfs = BFS(problem=problem)
path = bfs.run()
goal = problem.goals.pop()
print(path.get(goal))