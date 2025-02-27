from f_graph.path.generators.g_graph_map import GenGraphMap
from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne, TypeAlgo
import pandas as pd


import pandas as pd

folder = 'g:\\temp\\boundary\\maps'
graphs = GenGraphMap.maps_in_folder(path=folder, verbose=True)

# Collect data as a list of dictionaries
data = []

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
