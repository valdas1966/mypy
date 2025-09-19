from f_graph.path.algos.many_to_one.generators.g_problem import GenProblemManyToOne
from f_graph.path.algos.many_to_one.algo import AlgoManyToOne, TypeAlgo
from random import randint


def run(rows: int, num_starts: int, epochs: int) -> None:
    counter = 0
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
        if delta < 0:
            print(f'Explored [without]: {solution_without_boundary.explored}')
            print(f'Explored [with]: {solution_with_boundary.explored}')
            print('The graph:')
            print(problem.graph.grid)
            print('The starts:')
            print([node.uid.to_tuple() for node in solution_with_boundary.order])
            print('The goal:')
            print(problem.goal.uid.to_tuple())
            for node, state in solution_without_boundary.states.items():
                print(f'Explored [without]: {node.uid.to_tuple()}')
                print([node.uid.to_tuple() for node in state.explored])
            for node, state in solution_with_boundary.states.items():
                print(f'Explored [with]: {node.uid.to_tuple()}')
                print([node.uid.to_tuple() for node in state.explored])
            break
            # counter += 1
        if i % 1000 == 0:
            print(f'[{i} / {epochs}], [{round(i / epochs * 100)}%]')

    """
    print(f'rows: {rows}, counter: {counter}, pct: '
          f'{round(counter / epochs * 100, 2)}')
    """


for rows in [5]:
    for num_starts in [2]:
        run(rows=rows, num_starts=num_starts, epochs=1000000)
