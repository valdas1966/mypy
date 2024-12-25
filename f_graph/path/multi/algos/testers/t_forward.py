from f_graph.path.multi.algos.forward import Forward, ProblemMulti
from f_graph.path.single.algos.bfs import BFS
from f_graph.path.single.algos.a_star import AStar
from collections import Counter


def test_kx_bfs():
    problem = ProblemMulti.gen_3x3()
    problems = problem.to_singles()
    sols = {problem.goal: BFS(problem=problem).run() for problem in problems}
    paths_true = {goal: sols[goal].path for goal in sols.keys()}
    generated_true = sum(len(sol.state.generated) for goal, sol in sols)
    explored_true = sum(len(sol.state.explored) for goal, sol in sols)
    sol_multi = Forward(problem=problem,
                        type_algo=BFS,
                        is_shared=False).run()
    assert paths_true == {goal: sol.path for goal, sol in sol_multi}
    # assert solution.state.generated == generated_true
    # assert solution.state.explored == explored_true


def test_kx_bfs_shared():
    problem = Problem.gen_3x3()
    problems = problem.to_singles()
    sols = {problem.goal: BFS(problem=problem).run() for problem in problems}
    paths_true = {goal: sols[goal].path for goal in sols.keys()}
    generated_true = Counter([node for sol in sols.values()
                              for node in sol.state.generated])
    explored_true = Counter([node for sol in sols.values()
                             for node in sol.state.explored])
    solution = Forward(problem=problem,
                       type_algo=BFS,
                       is_shared=True).run()
    assert solution.paths == paths_true
    #assert solution.state.generated == generated_true
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
    solution = Forward(problem=problem,
                       type_algo=AStar,
                       is_shared=False).run()
    assert solution.paths == paths_true
    assert solution.state.generated == generated_true
    assert solution.state.explored == explored_true
