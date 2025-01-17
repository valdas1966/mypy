from f_graph.path.multi.algos.forward import ForwardMulti, ProblemMulti
from f_graph.path.one_to_one.algos.bfs import BFS
from f_graph.path.one_to_one.algos.a_star import AStar


def test_kx_bfs():
    problem = ProblemMulti.gen_3x3()
    problems = problem.to_singles()
    solutions_single = {problem.goal: BFS(problem=problem).run()
                        for problem in problems}
    paths_true = {goal: solutions_single[goal].path
                  for goal in solutions_single}
    solution_multi = ForwardMulti(problem=problem,
                                  type_algo=BFS,
                                  is_shared=False).run()
    assert paths_true == solution_multi.paths
    assert solution_multi.explored == 11


def test_kx_bfs_shared():
    problem_multi = ProblemMulti.gen_3x3()
    problems_single = problem_multi.to_singles()
    solutions_single = {problem.goal: BFS(problem=problem).run()
                        for problem in problems_single}
    paths_true = {goal: solutions_single[goal].path
                  for goal in solutions_single}
    solution_multi = ForwardMulti(problem=problem_multi,
                                  type_algo=BFS,
                                  is_shared=True).run()
    assert solution_multi.paths == paths_true
    assert solution_multi.explored == 8


def test_kx_astar():
    problem_multi = ProblemMulti.gen_3x3()
    problems_single = problem_multi.to_singles()
    solutions_single = {problem.goal: AStar(problem=problem).run()
                        for problem in problems_single}
    paths_true = {goal: solutions_single[goal].path
                  for goal in solutions_single}
    solution_multi = ForwardMulti(problem=problem_multi,
                                  type_algo=AStar,
                                  is_shared=False).run()
    assert solution_multi.paths == paths_true
    assert solution_multi.explored == 6


def test_kx_astar_shared():
    problem_multi = ProblemMulti.gen_3x3()
    problems_single = problem_multi.to_singles()
    solutions_single = {problem.goal: AStar(problem=problem).run()
                        for problem in problems_single}
    paths_true = {goal: solutions_single[goal].path
                  for goal in solutions_single}
    solution_multi = ForwardMulti(problem=problem_multi,
                                  type_algo=AStar,
                                  is_shared=True).run()
    assert solution_multi.paths == paths_true
    assert solution_multi.explored == 4
    