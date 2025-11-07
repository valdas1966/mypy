from f_graph.old_path.generators.g_graph import GenGraphPath as GenGraph
from f_graph.old_path.algos.many_to_one.generators.g_problem import GenProblemManyToOne as GenProblem
from f_graph.old_path.algos.many_to_one.problem import ProblemManyToOne as Problem
from f_graph.old_path.algos.many_to_one.algo import AlgoManyToOne as Algo, Solution
from datetime import datetime
from random import randint


def run(rows: int, epochs: int) -> None:
    """
    ========================================================================
     Run.
    ========================================================================
    """
    examples: list[tuple[Problem, int]] = list()
    for i in range(epochs):
        pct_invalid = randint(0, 75)
        graph = GenGraph.gen_random(rows=rows, pct_invalid=pct_invalid)
        problem = GenProblem.for_experiments(graph=graph, n_starts=2)
        algos: dict[int, Algo] = dict()
        sols: dict[int, Solution] = dict()
        for depth in (1, 2):
            algos[depth] = Algo(problem=problem, depth_boundary=depth)
            sols[depth] = algos[depth].run()
        delta = sols[1].explored - sols[2].explored
        if delta > 0:
            examples.append((problem, delta))
        if i % 1000 == 0:
            print(f'[{datetime.now()}] [{i} / {epochs}] [{len(examples)} examples found]')
    # return example with the highest difference in explored old_nodes
    examples_top: tuple[Problem, int] = sorted(examples, key=lambda x: x[1],
                                               reverse=True)[:5]
    for i, ex in enumerate(examples_top):
        problem, delta = ex
        print(f'Example #{i+1} with Delta: {delta}')
        print(f'Starts: {problem.starts}')
        print(f'Goal: {problem.goal}')
        print(problem.graph)
        print()


run(rows=4, epochs=100000)
