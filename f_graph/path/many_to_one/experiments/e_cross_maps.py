from f_graph.path.generators.g_graph_map import GenGraphMap, GraphMap
from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne
from f_graph.path.many_to_one.problem import ProblemManyToOne as Problem
from f_graph.path.many_to_one.algo import AlgoManyToOne, TypeAlgo
from f_psl.os.u_folder import UFolder
from f_utils import u_pickle
from datetime import datetime
import pandas as pd


cd = 'g'
folder_maps = f'{cd}:\\temp\\boundary\\maps'
folder_graphs = f'{cd}:\\temp\\boundary\\graphs'
pickle_graphs = f'{cd}:\\temp\\boundary\\maps.pkl'
pickle_problems = f'{cd}:\\temp\\boundary\\problems.pkl'
csv_results = f'{cd}:\\temp\\boundary\\results.csv'


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
            for _ in range(1):
                problem = GenProblemManyToOne.for_experiments(graph=graph,
                                                              n_starts=n_starts)
                t = (graph.name, problem.starts, problem.goal)
                problems.append(t)
            print(datetime.now().strftime("%H:%M:%S"),
                  f"[{i}/{len(paths_graphs)}] {graph.name} {n_starts}")
    u_pickle.dump(obj=problems, path=pickle_problems)


def experiments_to_csv() -> None:
    """
    ========================================================================
     Run the experiments and save the results to a csv file.
    ========================================================================
    """
    problems = u_pickle.load(path=pickle_problems)
    df = pd.DataFrame(columns=['domain', 'map', 'n_starts', 'density_start',
                               'elapsed_with', 'explored_with',
                               'h_start_goal', 'd_start_goal',
                               'elapsed_without', 'explored_without'])
    for i, problem in enumerate(problems):
        graph_name, starts, goal = problem
        pickle_graph = f'{folder_graphs}\\{graph_name}.pkl'
        graph = u_pickle.load(path=pickle_graph)
        problem = Problem(graph=graph, starts=starts, goal=goal)
        row = {'domain': problem.graph.domain,
               'map': problem.graph.name,
               'n_starts': len(problem.starts)}
        row['density_start'] = problem.graph.distance_avg(nodes=problem.starts)
        algo_without = AlgoManyToOne(problem=problem,
                                     type_algo=TypeAlgo.A_STAR,
                                     is_shared=True,
                                     with_boundary=False)
        sol_without = algo_without.run()
        row['elapsed_without'] = round(sol_without.elapsed, 2)
        row['explored_without'] = sol_without.explored
        algo_with = AlgoManyToOne(problem=problem,
                                  type_algo=TypeAlgo.A_STAR,
                                  is_shared=True,
                                  with_boundary=True)
        sol_with = algo_with.run()
        row['elapsed_with'] = round(sol_with.elapsed, 2)
        row['explored_with'] = sol_with.explored
        start_first = problem.starts[0]
        row['h_start_goal'] = problem.graph.distance(node_a=start_first,
                                                     node_b=problem.goal)
        row['d_start_goal'] = len(sol_with.paths[start_first])
        df = df._append(row, ignore_index=True)
        print(datetime.now().strftime("%H:%M:%S"),
              f'[{i}/{len(problems)}]')
    df.to_csv(csv_results, index=False)


# graphs_to_pickle()
# problems_to_pickle()
experiments_to_csv()
