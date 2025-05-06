from f_file.i_1_csv import CSV
from f_math.u_percent import UPercent
from f_psl.os.u_folder import UFolder
from f_psl.pandas.u_df import UDF, TypeAgg, TypeComparison
from f_psl.pandas.u_pivot import UPivot
from f_dv.i_1_bar import Bar
from f_dv.i_1_bar_stacked import BarStacked
from f_dv.i_1_scatter import Scatter
from f_dv.i_1_scatter_regression import ScatterRegression
from f_dv.i_1_heat_map import HeatMap
from f_color.rgb import RGB
import pandas as pd


cd = 'd'
folder = f'{cd}:\\temp\\boundary\\grands'
folder_results = f'{folder}\\results'
csv_results = f'{folder}\\results.csv'
csv_results_10 = f'{folder}\\results_10.csv'
csv_results_temp = f'{folder}\\results_temp.csv'
png_performance_comparison_by_depth = f'{folder_results}\\performance_comparison_by_depth.png'
png_exploration_reduction_by_depth = f'{folder_results}\\exploration_reduction_by_depth.png'
png_changed_nodes_by_depth = f'{folder_results}\\changed_nodes_by_depth.png'
png_time_reduction_by_depth = f'{folder_results}\\time_reduction_by_depth.png'
png_correlation_explored_elapsed = f'{folder_results}\\correlation_explored_elapsed.png'
png_explored_by_nodes_cnt = f'{folder_results}\\explored_by_nodes_cnt.png'
png_explored_by_nodes_pct = f'{folder_results}\\explored_by_nodes_pct.png'
png_explored_by_pct_nodes_cnt = f'{folder_results}\\explored_by_pct_nodes_cnt.png'
png_explored_by_pct_nodes_pct = f'{folder_results}\\explored_by_pct_nodes_pct.png'
png_explored_by_manhattan_distance_cnt = f'{folder_results}\\explored_by_manhattan_distance_cnt.png'
png_explored_by_manhattan_distance_pct = f'{folder_results}\\explored_by_manhattan_distance_pct.png'
png_explored_by_pct_start_goal_cnt = f'{folder_results}\\explored_by_pct_start_goal_cnt.png'
png_explored_by_pct_start_goal_pct = f'{folder_results}\\explored_by_pct_start_goal_pct.png'    
png_explored_by_goals = f'{folder_results}\\explored_by_goals.png'
png_explored_by_heuristic_quality_cnt = f'{folder_results}\\explored_by_heuristic_quality_cnt.png'
png_explored_by_heuristic_quality_pct = f'{folder_results}\\explored_by_heuristic_quality_pct.png'
png_normalized_manhattan_cnt = f'{folder_results}\\normalized_manhattan_cnt.png'
png_normalized_manhattan_pct = f'{folder_results}\\normalized_manhattan_pct.png'


def union_csv() -> None:
    """
    ========================================================================
     Union the csv files.
    ========================================================================
    """
    paths_from = UFolder.filepaths(path=folder_results)
    CSV.union(paths_from=paths_from, path_to=csv_results)


def format_csv() -> None:
    """
    ========================================================================
     Format the csv file.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_explored_1'] = round((1-df['pct_explored_1']) * 100)
    df['pct_explored_2'] = round((1-df['pct_explored_2']) * 100)
    df['pct_explored_3'] = round((1-df['pct_explored_3']) * 100)
    df['pct_explored_4'] = round((1-df['pct_explored_4']) * 100)
    df['pct_explored_5'] = round((1-df['pct_explored_5']) * 100)
    df['pct_elapsed_1'] = round((1-df['pct_elapsed_1']) * 100)
    df['pct_elapsed_2'] = round((1-df['pct_elapsed_2']) * 100)
    df['pct_elapsed_3'] = round((1-df['pct_elapsed_3']) * 100)
    df['pct_elapsed_4'] = round((1-df['pct_elapsed_4']) * 100)
    df['pct_elapsed_5'] = round((1-df['pct_elapsed_5']) * 100)
    df['pct_nodes'] = round(df['pct_nodes'] * 100)
    df.to_csv(csv_results, index=False)


def performance_comparison_by_depth() -> None:
    """
    ========================================================================
     Show the percentage of comparison.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    better_1 = UDF.count_comparison(df=df,
                                    col_a='explored_0',
                                    col_b='explored_1',
                                    type_cmp=TypeComparison.GREATER)
    equal_1 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_1',
                                   type_cmp=TypeComparison.EQUAL)
    worse_1 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_1',
                                   type_cmp=TypeComparison.LESS)
    better_2 = UDF.count_comparison(df=df,
                                    col_a='explored_0',
                                    col_b='explored_2',
                                    type_cmp=TypeComparison.GREATER)
    equal_2 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_2',
                                   type_cmp=TypeComparison.EQUAL)
    worse_2 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_2',
                                   type_cmp=TypeComparison.LESS)
    better_3 = UDF.count_comparison(df=df,
                                    col_a='explored_0',
                                    col_b='explored_3',
                                    type_cmp=TypeComparison.GREATER)
    equal_3 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_3',
                                   type_cmp=TypeComparison.EQUAL)   
    worse_3 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_3',
                                   type_cmp=TypeComparison.LESS)    
    better_4 = UDF.count_comparison(df=df,
                                    col_a='explored_0',
                                    col_b='explored_4',
                                    type_cmp=TypeComparison.GREATER)
    equal_4 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_4',
                                   type_cmp=TypeComparison.EQUAL)
    worse_4 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_4',
                                   type_cmp=TypeComparison.LESS)        
    better_5 = UDF.count_comparison(df=df,
                                    col_a='explored_0',
                                    col_b='explored_5',
                                    type_cmp=TypeComparison.GREATER)
    equal_5 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_5',
                                   type_cmp=TypeComparison.EQUAL)
    worse_5 = UDF.count_comparison(df=df,
                                   col_a='explored_0',
                                   col_b='explored_5',
                                   type_cmp=TypeComparison.LESS)
    name_labels = 'Depth'
    name_values = 'Percentage of Cases'
    x = ['1', '2', '3', '4', '5']
    pcts_1 = UPercent.to_pct([better_1, equal_1, worse_1])
    pcts_2 = UPercent.to_pct([better_2, equal_2, worse_2])
    pcts_3 = UPercent.to_pct([better_3, equal_3, worse_3])
    pcts_4 = UPercent.to_pct([better_4, equal_4, worse_4])
    pcts_5 = UPercent.to_pct([better_5, equal_5, worse_5])
    y = [pcts_1, pcts_2, pcts_3, pcts_4, pcts_5]
    d_stack = {'Better': RGB('LIGHT_GREEN'),
               'Equal': RGB('LIGHT_YELLOW'),
               'Worse': RGB('LIGHT_RED')}
    # name = 'Performance Comparison at Varying Depths'
    chart = BarStacked(x=x,
                       y=y,
                       d_stack=d_stack,
                       name_labels=name_labels,
                       name_values=name_values,
                       is_pct=True)
    chart.save(path=png_performance_comparison_by_depth)


def exploration_reduction_by_depth() -> None:
    """
    ========================================================================
     Show the percentage of explored cells.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    x = ['1', '2', '3', '4', '5']
    cols = ['pct_explored_1', 'pct_explored_2',
            'pct_explored_3', 'pct_explored_4', 'pct_explored_5']
    y = UDF.agg_cols(df=df, cols=cols, type_agg=TypeAgg.MEDIAN)
    name_x = 'Depth'
    name = '%Exploration Reduction'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_exploration_reduction_by_depth)


def time_reduction_by_depth() -> None:
    """
    ========================================================================
     Show the percentage of elapsed time.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    x = ['1', '2', '3', '4', '5']
    cols = ['pct_elapsed_1', 'pct_elapsed_2', 'pct_elapsed_3',
            'pct_elapsed_4', 'pct_elapsed_5']
    y = UDF.agg_cols(df=df, cols=cols, type_agg=TypeAgg.MEDIAN)
    name_x = 'Depth'
    name = '%Time Reduction'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_time_reduction_by_depth)


def correlation_explored_elapsed() -> None:
    """
    ========================================================================
     Show the correlation between explored and elapsed.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df = df[df['pct_explored_1'] >= -100]
    df = df[df['pct_explored_1'] <= 100]
    df = df[df['pct_elapsed_1'] >= -100]
    df = df[df['pct_elapsed_1'] <= 100]
    scatter = ScatterRegression(df=df,
                                col_x='pct_explored_1',
                                col_y='pct_elapsed_1',
                                label_x='Explored',
                                label_y='Elapsed',
                                name='Correlation of Explored vs Elapsed',
                                is_pct=True)
    scatter.save(path=png_correlation_explored_elapsed)


def changed_nodes_by_depth() -> None:
    """
    ========================================================================
     Show the changed.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_changed_1'] = round(df['changed_1'] / df['nodes'] * 100, 2)
    df['pct_changed_2'] = round(df['changed_2'] / df['nodes'] * 100, 2)
    df['pct_changed_3'] = round(df['changed_3'] / df['nodes'] * 100, 2)
    df['pct_changed_4'] = round(df['changed_4'] / df['nodes'] * 100, 2)
    df['pct_changed_5'] = round(df['changed_5'] / df['nodes'] * 100, 2)
    df = df[['pct_changed_1', 'pct_changed_2', 'pct_changed_3',
             'pct_changed_4', 'pct_changed_5']]
    x = ['1', '2', '3', '4', '5']
    cols = ['pct_changed_1', 'pct_changed_2', 'pct_changed_3',
            'pct_changed_4', 'pct_changed_5']
    y = UDF.agg_cols(df=df, cols=cols, type_agg=TypeAgg.MEDIAN)
    name_x = 'Depth'
    name = '%Changed Nodes'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_changed_nodes_by_depth)


def explored_by_nodes_cnt() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df = UDF.group_and_agg(df=df,
                           col_group='nodes',
                           multiple_group=100000)
    df = df.sort_values(by='nodes') 
    x = [str(int(val//1000)+100) for val in df['nodes'].tolist()]
    y = df['pct'].tolist()
    name_x = 'Nodes in Thousands'
    name = '%Experiments'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_explored_by_nodes_cnt)


def explored_by_nodes_pct() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df = UDF.group_and_agg(df=df,
                           col_group='nodes',
                           col_agg='pct_explored_2',
                           multiple_group=100000,
                           type_agg=TypeAgg.MEAN)
    x = [str(int(val//1000)+100) for val in df['nodes'].tolist()]
    y = df['pct_explored_2'].tolist()
    name_x = 'Nodes in Thousands'
    name = '%Reduced Exploration'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_explored_by_nodes_pct)


def explored_by_pct_nodes_cnt() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_nodes'] = round((1-df['pct_nodes']) * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='pct_nodes',
                           multiple_group=10)
    df = df.sort_values(by='pct_nodes') 
    x = df['pct_nodes'].tolist()
    y = df['pct'].tolist()
    name_x = 'Percentage of Obstacle-Density'
    name = '%Experiments'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_explored_by_pct_nodes_cnt)


def explored_by_pct_nodes_pct() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_nodes'] = round((1-df['pct_nodes']) * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='pct_nodes',
                           col_agg='pct_explored_2',
                           multiple_group=10,
                           type_agg=TypeAgg.MEAN)
    x = df['pct_nodes'].tolist()
    y = df['pct_explored_2'].tolist()
    name_x = 'Percentage of Obstacle-Density'
    name = '%Reduced Exploration'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_explored_by_pct_nodes_pct)


def explored_by_manhattan_distance_cnt() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_nodes'] = round((1-df['pct_nodes']) * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='h_start_goal',
                           multiple_group=400)
    df = df.sort_values(by='h_start_goal') 
    x = [str(int(val)+400) for val in df['h_start_goal'].tolist()]
    y = df['pct'].tolist()
    name_x = 'Manhattan Distance'
    name = '%Experiments'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_explored_by_manhattan_distance_cnt)


def explored_by_manhattan_distance_pct() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_nodes'] = round((1-df['pct_nodes']) * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='h_start_goal',
                           col_agg='pct_explored_2',
                           multiple_group=400,
                           type_agg=TypeAgg.MEAN)
    print(df)
    x = [str(int(val)+400) for val in df['h_start_goal'].tolist()]
    y = df['pct_explored_2'].tolist()
    name_x = 'Manhattan Distance'
    name = '%Reduced Exploration'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_explored_by_manhattan_distance_pct)


def normalized_manhattan_cnt() -> None:
    """
    ========================================================================
     Show the normalized manhattan distance.
    ========================================================================
    """
    df = pd.read_csv(csv_results_10)
    df['normalized_manhattan'] = round((df['h_start_goal'] / (df['rows'] + df['cols'] - 2)) * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='normalized_manhattan',
                           multiple_group=10)
    x = df['normalized_manhattan'].tolist()
    x = [str(int(val)) for val in x]
    y = df['pct'].tolist()
    name_x = 'Normalized Manhattan-Distance'
    name = '%Experiments'
    bar = Bar(x=x,
              y=y,
              name_x=name_x,
              name=name,
              is_y_pct=True)
    bar.save(path=png_normalized_manhattan_cnt)


def normalized_manhattan_pct() -> None:
    """
    ========================================================================
     Show the normalized manhattan distance.
    ========================================================================
    """
    df = pd.read_csv(csv_results_10)
    df['normalized_manhattan'] = round((df['h_start_goal'] / (df['rows'] + df['cols'] - 2)) * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='normalized_manhattan',
                           col_agg='pct_explored_2',
                           multiple_group=10,
                           type_agg=TypeAgg.MEAN)
    print(df)
    x = df['normalized_manhattan'].tolist()
    x = [str(int(val)) for val in x]
    y = df['pct_explored_2'].tolist()
    name_x = 'Normalized Manhattan-Distance'
    name = '%Reduced Exploration'
    bar = Bar(x=x,
              y=y,
              name_x=name_x,
              name=name,
              is_y_pct=True)
    bar.save(path=png_normalized_manhattan_pct)


def explored_by_goals() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results_10)
    df['pct_explored_2'] = round((1-df['pct_explored_2']) * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='goals',
                           col_agg='pct_explored_2',
                           multiple_group=2,
                           type_agg=TypeAgg.MEAN)
    x = df['goals'].tolist()
    y = df['pct_explored_2'].tolist()
    name_x = 'Number of Goals'
    name = '%Reduced Exploration'
    bar = Bar(x=x,
              y=y,
              name_x=name_x,
              name=name,
              is_y_pct=True)
    bar.save(path=png_explored_by_goals)


def explored_by_heuristic_quality_cnt() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_start_goal'] = round(df['pct_start_goal'] * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='pct_start_goal',
                           multiple_group=10)
    df['pct_start_goal'] = df['pct_start_goal'].astype(int)
    df = df.sort_values(by='pct_start_goal') 
    x = df['pct_start_goal'].tolist()
    y = df['pct'].tolist()
    name_x = 'Heuristic Quality'
    name = '%Experiments'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_explored_by_heuristic_quality_cnt)


def explored_by_heuristic_quality_pct() -> None:
    """
    ========================================================================
     Show the explored by nodes.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_start_goal'] = round(df['pct_start_goal'] * 100)
    df = UDF.group_and_agg(df=df,
                           col_group='pct_start_goal',
                           col_agg='pct_explored_2',
                           multiple_group=10,
                           type_agg=TypeAgg.MEAN)
    df['pct_start_goal'] = df['pct_start_goal'].astype(int)
    df = df.sort_values(by='pct_start_goal') 
    x = df['pct_start_goal'].tolist()
    y = df['pct_explored_2'].tolist()
    name_x = 'Heuristic Quality'
    name = '%Reduced Exploration'
    bar = Bar(x=x, y=y,
              name_x=name_x, name=name, is_y_pct=True)
    bar.save(path=png_explored_by_heuristic_quality_pct)


# union_csv()
# format_csv()
# performance_comparison_by_depth()
# exploration_reduction_by_depth()
# time_reduction_by_depth()
# correlation_explored_elapsed()
# changed_nodes_by_depth()
# explored_by_nodes_cnt()
# explored_by_nodes_pct()
# explored_by_pct_nodes_cnt()
# explored_by_pct_nodes_pct()
# explored_by_manhattan_distance_cnt()
# explored_by_manhattan_distance_pct()
# explored_by_goals()
# explored_by_heuristic_quality_cnt()
# explored_by_heuristic_quality_pct()
normalized_manhattan_cnt()
normalized_manhattan_pct()

