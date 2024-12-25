from f_graph.path.multi.algos.iterative import Iterative, Problem
from f_graph.path.single.algos.bfs import BFS


problem = Problem.gen_3x3()
print('Problem:')
print('====================')
print(problem)
print()

print(len(Iterative(problem=problem,
                    type_algo=BFS,
                    is_shared=False).run().state.explored))

print(len(Iterative(problem=problem,
                    type_algo=BFS,
                    is_shared=True).run().state.explored))
