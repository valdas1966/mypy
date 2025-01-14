from f_graph.path.multi.algos.forward import ForwardMulti, ProblemMulti
from f_graph.path.single.algos.bfs import BFS
from f_graph.path.single.algos.a_star import AStar
from collections import Counter


def test_kx_bfs():
    problem = ProblemMulti.gen_3x3()
    problems = problem.to_singles()
    solutions_single = {problem.goal: BFS(problem=problem).run()
                        for problem in problems}
    paths_true = {goal: solutions_single[goal].path
                  for goal in solutions_single}
    generated_true = sum(len(sol.state.generated) for sol in solutions_single.values())
    explored_true = sum(len(sol.state.explored) for sol in solutions_single.values())
    solution_multi = ForwardMulti(problem=problem,
                                  type_algo=BFS,
                                  is_shared=False).run()
    assert paths_true == solution_multi.paths
    assert solution_multi.generated == generated_true
    assert solution_multi.explored == explored_true


def test_kx_bfs_shared():
    problem = ProblemMulti.gen_3x3()
    problems = problem.to_singles()
    sols = {problem.goal: BFS(problem=problem).run() for problem in problems}
    paths_true = {goal: sols[goal].path for goal in sols}
    generated_true = Counter([node for sol in sols.values()
                              for node in sol.state.generated])
    explored_true = Counter([node for sol in sols.values()
                             for node in sol.state.explored])
    solution_multi = ForwardMulti(problem=problem,
                                  type_algo=BFS,
                                  is_shared=True).run()
    assert solution_multi.paths == paths_true
    assert solution_multi.generated == generated_true
    #assert solution.state.explored == explored_true


def test_kx_astar():
    problem = Problem.gen_3x3()
    problems = problem.to_singles()
    sols = {problem.goal: AStar(problem=problem).run() for problem in problems}
    paths_true = {goal: sols[goal].path for goal in sols.keys()}
    generated_true = Counter([node for sol in sols.values()
                              for node in sol.state.generated])
    explored_true = Counter([node for sol in sols.values()
                             for node in sol.state.explored])
    solution = ForwardMulti(problem=problem,
                            type_algo=AStar,
                            is_shared=False).run()
    assert solution.paths == paths_true
    assert solution.state.generated == generated_true
    assert solution.state.explored == explored_true
