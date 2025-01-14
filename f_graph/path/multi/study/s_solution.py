from f_graph.path.multi.solution import SolutionMulti, SolutionSingle
from f_graph.path.multi.problem import ProblemMulti
from f_graph.path.multi.algos.forward import ForwardMulti
from f_graph.path.single.algos.a_star import AStar
from f_graph.path.single.algos.bfs import BFS
from collections import Counter


problem = ProblemMulti.gen_3x3()
solution = ForwardMulti(problem=problem, type_algo=BFS, is_shared=True).run()
print(solution.state)


problem = ProblemMulti.gen_3x3()
problems = problem.to_singles()
sols = {problem.goal: BFS(problem=problem).run() for problem in problems}
generated_true = Counter([node for sol in sols.values()
                              for node in sol.state.generated])


c = Counter([1, 1, 2])
print(c)
