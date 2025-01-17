from f_graph.path.multi.algos.forward import ForwardMulti, ProblemMulti
from f_graph.path.one_to_one.algos.bfs import BFS
from f_graph.path.one_to_one.algos.a_star import AStar
from collections import Counter


type_algo = BFS
problem_multi = ProblemMulti.gen_3x3()
problems_single = problem_multi.to_singles()
solutions_single = {problem.goal: type_algo(problem=problem).run()
                    for problem in problems_single}

solution_multi = ForwardMulti(problem=problem_multi,
                              type_algo=type_algo,
                              is_shared=True).run()
print(solution_multi.explored)
