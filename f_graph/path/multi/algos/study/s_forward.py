from f_graph.path.multi.algos.forward import ForwardMulti, Problem
from f_graph.path.single.algos.bfs import BFS


problem = Problem.gen_3x3()
print('Problem:')
print('====================')
print(problem)
print()

kbfs = ForwardMulti(problem=problem, type_algo=BFS, is_shared=True)
solution = kbfs.run()
print(solution.path)

