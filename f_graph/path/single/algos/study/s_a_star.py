from f_graph.path.single.algos.a_star import AStar, Problem


problem = Problem.gen_3x3()
graph = problem.graph
astar = AStar(problem=problem)
solution = astar.run()
print(solution.path)
