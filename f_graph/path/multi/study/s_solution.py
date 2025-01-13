from f_graph.path.multi.solution import SolutionMulti, SolutionSingle
from f_graph.path.multi.problem import ProblemMulti
from f_graph.path.multi.algos.forward import ForwardMulti
from f_graph.path.single.algos.a_star import AStar


problem = ProblemMulti.gen_3x3()
solution = ForwardMulti(problem=problem, type_algo=AStar, is_shared=True).run()
for goal, path in solution.paths.items():
    print(goal)
    print([node.uid for node in path])

