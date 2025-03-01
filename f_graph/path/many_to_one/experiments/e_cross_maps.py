from f_ds.graphs.i_2_grid import Graph
from f_graph.path.generators.g_graph_map import GenGraphMap, GraphMap
from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne, TypeAlgo, Node
from f_psl.os.u_folder import UFolder
from f_utils import u_pickle
from datetime import datetime
import pandas as pd


folder_maps = 'g:\\temp\\boundary\\maps'
folder_graphs = 'g:\\temp\\boundary\\graphs'
pickle_graphs = 'g:\\temp\\boundary\\maps.pkl'
pickle_problems = 'g:\\temp\\boundary\\problems.pkl'


def graphs_to_pickle() -> None:
    """
    ========================================================================
     Convert the maps to a pickle as a dict {Graph.Name -> GraphMap}.
    ========================================================================
    """
    maps_to_graphs = GenGraphMap.maps_in_folder
    graphs: dict[str, GraphMap] = maps_to_graphs(path=folder_maps,
                                                 verbose=True)
    for name, graph in graphs.items():
        path = f'{folder_graphs}\\{name}.pkl'
        u_pickle.dump(obj=graph, path=path)


def problems_to_pickle() -> None:
    """
    ========================================================================
     Convert the maps to a pickle as a list[tuple(str, set[Node], Node)].
    ========================================================================
    """
    problems: list[tuple] = list()
    paths_graphs = UFolder.filepaths(path=folder_graphs)
    for i, path in enumerate(paths_graphs):
        graph = u_pickle.load(path=path)
        for n_starts in [2, 4, 6, 8, 10]:
            for percentile in range(20, 101, 20):
                percentile_min = percentile - 19
                percentile_max = percentile
                print(percentile_min, percentile_max)
                problem = GenProblemManyToOne.for_experiments(graph=graph,
                                                              n_starts=n_starts,
                                                              percentile_min=percentile_min,
                                                              percentile_max=percentile_max)
                t = (graph.name, problem.starts, problem.goal)
                problems.append(t)
                print(datetime.now().strftime("%H:%M:%S"),
                      f"[{i}/{len(paths_graphs)}] {graph.name} {n_starts} {percentile}")
    u_pickle.dump(obj=problems, path=pickle_problems)


"""
data: list[dict] = dict()

for graph in graphs:
    for n_starts in [2, 4, 6, 8, 10]:
        row = {'domain': graph.domain, 'map': graph.name, 'n_starts': n_starts}

        # Generate the problem
        problem = GenProblemManyToOne.for_experiments(graph=graph,
                                                      n_starts=n_starts)
        row["density_start"] = graph.distance_avg(nodes=problem.starts)

        algo_with = AlgoManyToOne(problem=problem,
                                  type_algo=TypeAlgo.A_STAR,
                                  is_shared=True,
                                  with_boundary=True)
        solution_with = algo_with.run()
        row["elapsed_with"] = round(solution_with.elapsed, 2)
        row["explored_with"] = solution_with.explored

        start_first = solution_with.order[0]
        row["h_start_goal"] = problem.graph.distance(node_a=start_first,
                                                     node_b=problem.goal)
        row["d_start_goal"] = len(solution_with.paths[start_first])

        algo_without = AlgoManyToOne(problem=problem,
                                     type_algo=TypeAlgo.A_STAR,
                                     is_shared=True,
                                     with_boundary=False)
        solution_without = algo_without.run()
        row["elapsed_without"] = round(solution_without.elapsed, 2)
        row["explored_without"] = solution_without.explored

        print(row)
        data.append(row)  # Append dictionary to list

# Convert list of dictionaries to DataFrame **in one step**
df = pd.DataFrame(data)


# save the DataFrame
df.to_csv('g:\\temp\\boundary\\maps\\cross_maps.csv', index=False)
"""

# graphs_to_pickle()

problems_to_pickle()
