from f_graph.path.generators.g_graph import GenGraphPath as GenGraph, Graph
from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne as GenProblem
from f_graph.path.many_to_one.problem import ProblemManyToOne as Problem
from f_graph.path.many_to_one.algo import AlgoManyToOne
from f_ds.grids.grid import Grid, Cell
from f_utils import u_pickle
import pandas as pd
import random
from datetime import datetime


cd = 'g'
folder = f'{cd}:\\temp\\boundary\\grands'
pickle_problems = f'{folder}\\problems_4.pkl'
csv_results = f'{folder}\\results_4.csv'
folder_graphs = f'{cd}:\\temp\\boundary\\graphs'


def problems_to_pickle(n_problems: int, n_rows: int) -> None:
    """
    ========================================================================
     Pickle the problems.
    ========================================================================
    """
    graphs: list[Graph] = list()
    for _ in range(n_problems):
        pct_invalid = random.randint(10, 70)
        graph = GenGraph.gen_random(rows=n_rows,
                                    pct_invalid=pct_invalid)
        graphs.append(graph)
    problems: list[Problem] = list()
    for graph in graphs:
        problem = GenProblem.for_experiments(graph=graph,
                                             n_starts=10)
        problems.append(problem)
    u_pickle.dump(obj=problems, path=pickle_problems)


def experiments_to_csv() -> None:
    """
    ========================================================================
     Convert the problems to a csv.
    ========================================================================
    """
    df = pd.DataFrame(columns=['rows', 'nodes', 'pct_nodes', 'd_start_goal', 'h_start_goal', 'pct_start_goal',
                               'explored_0', 'elapsed_0', 'changed_0',
                               'explored_1', 'elapsed_1', 'pct_explored_1', 'pct_elapsed_1',
                               'explored_2', 'elapsed_2', 'pct_explored_2', 'pct_elapsed_2',
                               'explored_3', 'elapsed_3', 'pct_explored_3', 'pct_elapsed_3',
                               'explored_4', 'elapsed_4', 'pct_explored_4', 'pct_elapsed_4',
                               'explored_5', 'elapsed_5', 'pct_explored_5', 'pct_elapsed_5'])
    problems: list[Problem] = u_pickle.load(path=pickle_problems)
    for i, problem in enumerate(problems):
        print(f'[{datetime.now()}] {i}/{len(problems)}')
        row: dict[str, int|float] = {'rows': problem.graph.grid.rows,
                                     'nodes': len(problem.graph),
                                     'pct_nodes': round(len(problem.graph) / problem.graph.grid.rows*problem.graph.grid.rows, 2),
                                     'h_start_goal': problem.graph.distance(problem.starts[0], problem.goal)}
        for depth in range(3):
            algo = AlgoManyToOne(problem=problem,
                                 depth_boundary=depth)
            sol = algo.run()
            row['d_start_goal'] = len(sol.paths[problem.starts[0]])
            row['pct_start_goal'] = round(row['h_start_goal'] / row['d_start_goal'], 2) if row['d_start_goal'] else 0
            row[f'explored_{depth}'] = sol.explored
            row[f'elapsed_{depth}'] = sol.elapsed
            row[f'pct_explored_{depth}'] = round(row[f'explored_{depth}'] /
                                                 row[f'explored_{depth-1}'],
                                                 2) if depth and row[f'explored_{depth-1}'] else 0
            row[f'pct_elapsed_{depth}'] = round(row[f'elapsed_{depth}'] /
                                                row[f'elapsed_{depth-1}'],
                                                2) if depth and row[f'elapsed_{depth-1}'] else 0
        if row['d_start_goal']:
            df = df._append(row, ignore_index=True)
    df.to_csv(csv_results, index=False)


def cross_maps_to_csv() -> None:
    """
    ========================================================================
     Convert the problems to a csv.
    ========================================================================
    """
    df = pd.DataFrame(columns=['rows', 'cols','nodes', 'pct_nodes', 'd_start_goal', 'h_start_goal', 'pct_start_goal',
                               'explored_0', 'elapsed_0', 'changed_0',
                               'explored_1', 'elapsed_1', 'changed_1', 'pct_explored_1', 'pct_elapsed_1',
                               'explored_2', 'elapsed_2', 'changed_2', 'pct_explored_2', 'pct_elapsed_2',
                               'explored_3', 'elapsed_3', 'changed_3', 'pct_explored_3', 'pct_elapsed_3',
                               'explored_4', 'elapsed_4', 'changed_4', 'pct_explored_4', 'pct_elapsed_4',
                               'explored_5', 'elapsed_5', 'changed_5', 'pct_explored_5', 'pct_elapsed_5'])
    problems: list[Problem] = u_pickle.load(path=pickle_problems)
    for i, problem in enumerate(problems):
        graph_name, starts, goal = problem
        pickle_graph = f'{folder_graphs}\\{graph_name}.pkl'
        graph = u_pickle.load(path=pickle_graph)
        problem = Problem(graph=graph, starts=starts, goal=goal)
        row: dict[str, int|float] = {'rows': graph.grid.rows,
                                     'cols': graph.grid.cols,
                                     'nodes': len(problem.graph),
                                     'pct_nodes': round(len(problem.graph) /
                                                        (
                                                                graph.grid.rows*graph.grid.cols), 2),
                                     'h_start_goal': problem.graph.distance(problem.starts[0], problem.goal)}
        for depth in range(6):
            algo = AlgoManyToOne(problem=problem,
                                 depth_boundary=depth)
            sol = algo.run()
            row['d_start_goal'] = len(sol.paths[problem.starts[0]])
            row['pct_start_goal'] = round(row['h_start_goal'] / row['d_start_goal'], 2) if row['d_start_goal'] else 0
            row[f'explored_{depth}'] = sol.explored
            row[f'elapsed_{depth}'] = sol.elapsed
            row[f'pct_explored_{depth}'] = round(row[f'explored_{depth}'] /
                                                 row[f'explored_0'],
                                                 2) if depth and row[f'explored_{depth-1}'] else 0
            row[f'pct_elapsed_{depth}'] = round(row[f'elapsed_{depth}'] /
                                                row[f'elapsed_0'],
                                                2) if depth and row[f'elapsed_{depth-1}'] else 0
            row[f'changed_{depth}'] = sol.changed.get(depth, 0)
        if row['d_start_goal']:
            df = df._append(row, ignore_index=True)
            print(row['changed_0'], row['changed_1'], row['changed_2'], row['changed_3'], row['changed_4'], row['changed_5'])
        print(f'[{datetime.now()}] {i}/{len(problems)}')
    df.to_csv(csv_results, index=False)


def negative_example_to_pickle() -> None:
    """
    ========================================================================
     Pickle the negative example.
    ========================================================================
    """
    grid = Grid(rows=10)
    obstacles = [grid[0][3], grid[0][4], grid[0][5],
                grid[1][4], grid[3][3],
                grid[4][0], grid[4][1], grid[4][2], grid[4][3], grid[4][4],
                grid[5][0], grid[5][1], grid[5][2]]
    Cell.invalidate(cells=obstacles)
    graph = Graph(grid=grid)
    starts = [graph[1, 1], graph[2, 0]]
    goal = graph[5, 3]
    problem = Problem(graph=graph, starts=starts, goal=goal)
    u_pickle.dump(obj=[problem], path=pickle_problems)


def positive_example_to_pickle() -> None:
    """
    ========================================================================
     Pickle the positive example.
    ========================================================================
    """
    grid = Grid(rows=4)
    obstacles = [grid[1][2], grid[2][1], grid[3][1]]
    Cell.invalidate(cells=obstacles)
    graph = Graph(grid=grid)
    starts = [graph[0, 0], graph[1, 1]]
    goal = graph[3, 2]
    problem = Problem(graph=graph, starts=starts, goal=goal)
    u_pickle.dump(obj=[problem], path=pickle_problems)


# problems_to_pickle(n_rows=100, n_problems=100)
# positive_example_to_pickle()
# experiments_to_csv()
cross_maps_to_csv()
