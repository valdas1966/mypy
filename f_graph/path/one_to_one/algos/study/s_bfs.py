from f_graph.path.one_to_one.algos.bfs import BFS
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne

problem = GenProblemOneToOne.gen_3x3()
bfs = BFS(problem=problem)

