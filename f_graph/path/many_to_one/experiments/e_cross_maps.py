from f_graph.path.generators.g_graph_map import GenGraphMap
from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne, TypeAlgo
from dataclasses import dataclass


@dataclass
class DataExperiment:
    domain: str
    map: str
    n_starts: int
    h_starts_goal: int
    dist_starts_goal: int
    elapsed_with: int
    elapsed_without: int
    explored_with: int
    explored_without: int


folder = 'd:\\temp\\boundary\\maps'
graphs = GenGraphMap.maps_in_folder(path=folder, verbose=True)

for graph in graphs:
    for n_start in [2, 4, 6, 8, 10]:
        data = DataExperiment(domain=graph.domain,
                               map=graph.name,
                                 n_starts=n_start)
        problem = GenProblemManyToOne.for_experiments(graph=graph,
                                                       n_starts=2)
        algo_with = AlgoManyToOne(problem=problem,
                                  type_algo=TypeAlgo.A_STAR,
                                  is_shared=True,
                                  with_boundary=True)
        solution_with = algo_with.run()
        data.elapsed_with = solution_with.elapsed
        data.explored_with = solution_with.explored
        algo_without = AlgoManyToOne(problem=problem,
                                     type_algo=TypeAlgo.A_STAR,
                                     is_shared=True,
                                     with_boundary=False)
        solution_without = algo_without.run()
        data.elapsed_without = solution_without.elapsed
        data.explored_without = solution_without.explored

