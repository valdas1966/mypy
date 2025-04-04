from f_graph.path.many_to_one.algo import AlgoManyToOne as Algo, TypeAlgo
from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne as GenProblem
from f_graph.path.many_to_one.problem import ProblemManyToOne as Problem, Node
from f_graph.path.generators.g_graph import GenGraphPath
from datetime import datetime
from random import randint


rows = 6
epochs = 1000000
n_starts = 2


def run(rows: int, epochs: int) -> list[tuple[Problem, int, list[Node]]]:
    """
    ========================================================================
     Run.
    ========================================================================
    """
    def _gen_algo(problem: Problem, with_boundary: bool) -> Algo:
        """
        ====================================================================
         Generate an algorithm.
        ====================================================================
        """
        return Algo(problem=problem,
                    type_algo=TypeAlgo.A_STAR,
                    is_shared=True,
                    with_boundary=with_boundary)
    examples: list[tuple[Problem, int]] = list()
    for i in range(epochs):
        pct_invalid = randint(0, 50)
        graph = GenGraphPath.gen_random(rows=rows, pct_invalid=pct_invalid)
        problem = GenProblem.for_experiments(graph=graph, n_starts=n_starts)
        algo_with = _gen_algo(problem=problem, with_boundary=True)
        sol_with = algo_with.run()
        algo_without = _gen_algo(problem=problem, with_boundary=False)
        sol_without = algo_without.run()
        delta = sol_with.explored - sol_without.explored
        if delta > 0:
            start_1, start_2 = problem.starts
            if problem.graph.distance(start_1, start_2) > 0:
                example = (problem, delta)
                examples.append(example)
        if i % 1000 == 0:
            print(f'[{datetime.now()}] [{i} / {epochs}] [{len(examples)} examples found]')
    return examples


examples = run(rows=rows, epochs=epochs)
# return example with the highest difference in explored nodes
examples_top: tuple[Problem, int] = sorted(examples, key=lambda x: x[1],
                                           reverse=True)[:5]
# return example with the lowest difference in explored nodes
examples_bottom: tuple[Problem, int] = sorted(examples, key=lambda x: x[1])[:5]


for i, ex in enumerate(examples_top):
    problem, delta = ex
    print(f'Example #{i+1} with Delta: {delta}')
    print(f'Starts: {problem.starts}')
    print(f'Goal: {problem.goal}')
    print(problem.graph)
    print()

for i, ex in enumerate(examples_bottom):
    problem, delta = ex
    print(f'Example #{i+1} with Delta: {delta}')
    print(f'Starts: {problem.starts}')
    print(f'Goal: {problem.goal}')
    print(problem.graph)
    print()

"""
print('Example Top:')
problem_top, delta_top, order_top = example_top
print(f'Graph:')
print(problem_top.graph)
print(f'Starts: {order_top}')
print(f'Goal: {problem_top.goal}')
print(f'Delta: {delta_top}')

print('Example Bottom:')
problem_bottom, delta_bottom, order_bottom = example_bottom
print(f'Graph:')
print(problem_bottom.graph)
print(f'Starts: {order_bottom}')
print(f'Goal: {problem_bottom.goal}')
print(f'Delta: {delta_bottom}')
"""