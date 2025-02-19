from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne, TypeAlgo
from random import randint


def run(rows: int, epochs: int) -> None:
    num_starts = 2
    for i in range(epochs):
        pct_invalid = randint(0, 50)

        problem = GenProblemManyToOne.gen_random(rows=rows,
                                                 pct_invalid=pct_invalid,
                                                 num_starts=num_starts)
        algo_with_boundary = AlgoManyToOne(problem=problem,
                                           type_algo=TypeAlgo.A_STAR,
                                           is_eager=True,
                                           is_shared=True,
                                           with_boundary=True)
        solution_with_boundary = algo_with_boundary.run()
        algo_without_boundary = AlgoManyToOne(problem=problem,
                                              type_algo=TypeAlgo.A_STAR,
                                              is_shared=True,
                                              with_boundary=False)
        solution_without_boundary = algo_without_boundary.run()
        delta = solution_without_boundary.explored - solution_with_boundary.explored
        if delta > 0:
            print(solution_without_boundary.explored)
            print(solution_with_boundary.explored)
            print(problem.graph._grid)
            print([node.uid.to_tuple() for node in problem.starts])
            print(problem.goal.uid.to_tuple())
            break
        if i % 1000 == 0:
            print(f'[{i} / {epochs}]')


run(rows=4, epochs=1000000)
