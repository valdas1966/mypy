from f_graph.path.algo import Problem
from f_graph.path.generators.g_graph import GenGraphPath as GenGraph, Graph
from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne as GenProblem
from f_graph.path.many_to_one.problem import ProblemManyToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne
from f_graph.path.one_to_many.algo import AlgoOneToMany, AlgoOneToOne
from f_graph.path.one_to_many.problem import ProblemOneToMany, ProblemOneToOne
from f_graph.path.cache import Cache
from f_ds.grids.grid import Grid, Cell
from f_file.i_1_csv import CSV
from f_psl.os.u_folder import UFolder
from f_utils import u_pickle
import pandas as pd
import random
from datetime import datetime


cd = 'g'
folder = f'{cd}:\\temp\\boundary\\grands'
pickle_problems = f'{folder}\\problems_10.pkl'
csv_results = f'{folder}\\results_10.csv'
folder_graphs = f'{cd}:\\temp\\boundary\\graphs'
folder_results = f'{folder}\\results'
csv_results_union = f'{folder}\\results_union.csv'
csv_forward = f'{folder}\\forward.csv'


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
    titles = ['map', 'rows', 'cols', 'nodes', 'pct_nodes', 'goals',
              'd_start_goal', 'h_start_goal', 'pct_start_goal',
              'explored_0', 'explored_1', 'explored_2', 'explored_3',
              'explored_4', 'explored_5',
              'pct_explored_1', 'pct_explored_2', 'pct_explored_3',
              'pct_explored_4', 'pct_explored_5',
              'elapsed_0', 'elapsed_1', 'elapsed_2', 'elapsed_3',
              'elapsed_4', 'elapsed_5',
              'pct_elapsed_1', 'pct_elapsed_2', 'pct_elapsed_3',
              'pct_elapsed_4', 'pct_elapsed_5',
              'changed_0', 'changed_1', 'changed_2', 'changed_3',
              'changed_4', 'changed_5']
    csv = CSV(path=csv_results, titles=titles)
    problems: list[Problem] = u_pickle.load(path=pickle_problems)
    for i, p in enumerate(problems):
        graph_name, starts, goal = p
        pickle_graph = f'{folder_graphs}\\{graph_name}.pkl'
        graph = u_pickle.load(path=pickle_graph)
        problem = Problem(graph=graph, starts=starts, goal=goal)
        row: dict[str, str] = dict()
        row['map'] = graph.grid.name
        row['rows'] = graph.grid.rows
        row['cols'] = graph.grid.cols
        row['nodes'] = len(problem.graph)
        row['goals'] = len(problem.starts)
        total = graph.grid.rows * graph.grid.cols
        row['pct_nodes'] = round(row['nodes'] / total, 2)
        h_start_goal = problem.graph.distance(problem.starts[0], problem.goal)
        row['h_start_goal'] = h_start_goal
        for depth in range(6):
            algo = AlgoManyToOne(problem=problem,
                                 depth_boundary=depth)
            sol = algo.run()
            d_start_goal = len(sol.paths[problem.starts[0]])
            row['d_start_goal'] = d_start_goal
            if d_start_goal:
                row['pct_start_goal'] = round(h_start_goal / d_start_goal, 2)
            row[f'explored_{depth}'] = sol.explored
            row[f'elapsed_{depth}'] = sol.elapsed
            if depth:
                row[f'pct_explored_{depth}'] = round(sol.explored / row['explored_0'], 2)
                row[f'pct_elapsed_{depth}'] = round(sol.elapsed / row['elapsed_0'], 2)
                row[f'changed_{depth}'] = sol.changed.get(depth, 0)
        if d_start_goal:
            csv.write_dicts(dicts=[row])
            print(row['changed_1'], row['changed_2'], row['changed_3'], row['changed_4'], row['changed_5'])
        print(f'[{datetime.now()}] {i}/{len(problems)}')


def all_algo_to_csv() -> None:
    """
    ========================================================================
     Convert the problems to a csv.
    ========================================================================
    """
    titles = ['map', 'rows', 'cols', 'nodes', 'pct_nodes', 'goals',
              'd_start_goal', 'h_start_goal', 'pct_start_goal',
              'backward_0', 'backward_1', 'forward', 'bi', 'iterative']
    csv = CSV(path=csv_results, titles=titles)
    problems: list[Problem] = u_pickle.load(path=pickle_problems)
    for i, p in enumerate(problems):
        graph_name, starts, goal = p
        pickle_graph = f'{folder_graphs}\\{graph_name}.pkl'
        graph = u_pickle.load(path=pickle_graph)
        problem = Problem(graph=graph, starts=starts, goal=goal)
        row: dict[str, str] = dict()
        row['map'] = graph.grid.name
        row['rows'] = graph.grid.rows
        row['cols'] = graph.grid.cols
        row['nodes'] = len(problem.graph)
        row['goals'] = len(problem.starts)
        total = graph.grid.rows * graph.grid.cols
        row['pct_nodes'] = round(row['nodes'] / total, 2)
        h_start_goal = problem.graph.distance(problem.starts[0], problem.goal)
        row['h_start_goal'] = h_start_goal
        for depth in range(2):
            algo = AlgoManyToOne(problem=problem,
                                 depth_boundary=depth,
                                 verbose=False)
            sol = algo.run()
            d_start_goal = len(sol.paths[problem.starts[0]])
            row['d_start_goal'] = d_start_goal
            if d_start_goal:
                row['pct_start_goal'] = round(h_start_goal / d_start_goal, 2)
            row[f'backward_{depth}'] = sol.explored
        problem_cloned = problem.clone()
        problem_forward = ProblemOneToMany(graph=problem_cloned.graph,
                                           start=problem_cloned.goal,
                                           goals=problem_cloned.starts)
        algo_forward = AlgoOneToMany(problem=problem_forward, verbose=False)
        sol_forward = algo_forward.run()
        row['forward'] = sol_forward.explored
        algo_iterative = AlgoOneToMany(problem=problem_forward.clone(),
                                       is_shared=False,
                                       verbose=False)
        sol_iterative = algo_iterative.run()
        row['iterative'] = sol_iterative.explored
        goal_first = list(problem_forward.goals)[0].clone()
        problem_first = ProblemOneToOne(graph=problem_forward.graph,
                                        start=problem_forward.start,
                                        goal=goal_first)
        algo_first = AlgoOneToOne(problem=problem_first.clone(), verbose=False)
        sol_first = algo_first.run()
        cache_rest = Cache.from_explored(explored=sol_first.state.explored)
        problem_rest = problem_forward.clone()
        problem_rest.goals.remove(goal_first)
        algo_rest = AlgoManyToOne(problem=problem_rest,
                                  cache=cache_rest,
                                  verbose=False)
        sol_rest = algo_rest.run()
        row['bi'] = sol_first.stats.explored + sol_rest.explored
        if row['d_start_goal']:
            csv.write_dicts(dicts=[row])
        print(f'[{datetime.now()}] {i}/{len(problems)}')


def algo_forward() -> None:
    """
    ========================================================================
     Run the algo forward.
    ========================================================================
    """
    titles = ['forward']
    csv = CSV(path=csv_forward, titles=titles)
    problems: list[Problem] = u_pickle.load(path=pickle_problems)
    for i, p in enumerate(problems):
        graph_name, starts, goal = p
        pickle_graph = f'{folder_graphs}\\{graph_name}.pkl'
        graph = u_pickle.load(path=pickle_graph)
        problem = ProblemOneToMany(graph=graph, start=goal, goals=starts)
        algo = AlgoOneToMany(problem=problem)
        sol = algo.run()
        if sol:
            row: dict[str, str] = dict()
            row['forward'] = sol.explored
            csv.write_dicts(dicts=[row])
        print(f'[{datetime.now()}] {i}/{len(problems)}')
    

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


def union_csv() -> None:
    """
    ========================================================================
     Union the csv files.
    ========================================================================
    """
    paths_from = UFolder.filepaths(path=folder_results)
    CSV.union(paths_from=paths_from, path_to=csv_results_union)


# problems_to_pickle(n_rows=100, n_problems=100)
# positive_example_to_pickle()
# experiments_to_csv()
# cross_maps_to_csv()
# all_algo_to_csv()
# # union_csv()
algo_forward()
