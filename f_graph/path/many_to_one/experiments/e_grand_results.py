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


cd = 'g'
folder = f'{cd}:\\temp\\boundary\\grands'
folder_results = f'{folder}\\results'
csv_results = f'{folder}\\results.csv'
csv_results_temp = f'{folder}\\results_temp.csv'


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
    df.to_csv(csv_results, index=False)


def show_pct_comparison() -> None:
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
                                    col_a='explored_1',
                                    col_b='explored_2',
                                    type_cmp=TypeComparison.GREATER)
    equal_2 = UDF.count_comparison(df=df,
                                   col_a='explored_1',
                                   col_b='explored_2',
                                   type_cmp=TypeComparison.EQUAL)
    worse_2 = UDF.count_comparison(df=df,
                                   col_a='explored_1',
                                   col_b='explored_2',
                                   type_cmp=TypeComparison.LESS)
    better_3 = UDF.count_comparison(df=df,
                                    col_a='explored_2',
                                    col_b='explored_3',
                                    type_cmp=TypeComparison.GREATER)
    equal_3 = UDF.count_comparison(df=df,
                                   col_a='explored_2',
                                   col_b='explored_3',
                                   type_cmp=TypeComparison.EQUAL)   
    worse_3 = UDF.count_comparison(df=df,
                                   col_a='explored_2',
                                   col_b='explored_3',
                                   type_cmp=TypeComparison.LESS)    
    better_4 = UDF.count_comparison(df=df,
                                    col_a='explored_3',
                                    col_b='explored_4',
                                    type_cmp=TypeComparison.GREATER)
    equal_4 = UDF.count_comparison(df=df,
                                   col_a='explored_3',
                                   col_b='explored_4',
                                   type_cmp=TypeComparison.EQUAL)
    worse_4 = UDF.count_comparison(df=df,
                                   col_a='explored_3',
                                   col_b='explored_4',
                                   type_cmp=TypeComparison.LESS)        
    better_5 = UDF.count_comparison(df=df,
                                    col_a='explored_4',
                                    col_b='explored_5',
                                    type_cmp=TypeComparison.GREATER)
    equal_5 = UDF.count_comparison(df=df,
                                   col_a='explored_4',
                                   col_b='explored_5',
                                   type_cmp=TypeComparison.EQUAL)
    worse_5 = UDF.count_comparison(df=df,
                                   col_a='explored_4',
                                   col_b='explored_5',
                                   type_cmp=TypeComparison.LESS)
    name_labels = 'Depths'
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
    name = 'Performance Comparison at Varying Depths'
    chart = BarStacked(x=x,
                       y=y,
                       d_stack=d_stack,
                       name_labels=name_labels,
                       name_values=name_values,
                       is_pct=True,
                       name=name)
    chart.show()

def show_pct_comparison_to_zero() -> None:
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
    name_labels = 'Depths'
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
    name = 'Performance Comparison at Varying Depths'
    chart = BarStacked(x=x,
                       y=y,
                       d_stack=d_stack,
                       name_labels=name_labels,
                       name_values=name_values,
                       is_pct=True,
                       name=name)
    chart.show()

def show_pct_explored() -> None:
    """
    ========================================================================
     Show the percentage of explored cells.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    labels = ['1', '2', '3', '4', '5']
    cols = ['pct_explored_1', 'pct_explored_2',
            'pct_explored_3', 'pct_explored_4', 'pct_explored_5']
    values = UDF.agg_cols(df=df, cols=cols, type_agg=TypeAgg.MEDIAN)
    name_labels = 'Depth'
    name_values = 'Percentage of Exploration Reduction'
    bar = Bar(labels=labels, values=values,
              name_labels=name_labels, name_values=name_values, is_pct=True)
    bar.show()


def show_pct_explored_only_better() -> None:
    """
    ========================================================================
     Show the percentage of explored cells.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df = df[df['explored_1'] < df['explored_0']]
    labels = ['1', '2', '3', '4', '5']
    cols = ['pct_explored_1', 'pct_explored_2',
            'pct_explored_3', 'pct_explored_4', 'pct_explored_5']
    values = UDF.agg_cols(df=df, cols=cols, type_agg=TypeAgg.MEDIAN)
    name_labels = 'Depth'
    name_values = 'Percentage of Exploration Reduction'
    name = 'Exploration Reduction at Varying Depths'
    bar = Bar(labels=labels, values=values,
              name_labels=name_labels, name_values=name_values,
              is_pct=True, name=name)
    bar.show()


def show_pct_elapsed() -> None:
    """
    ========================================================================
     Show the percentage of elapsed time.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    labels = ['1', '2', '3', '4', '5']
    cols = ['pct_elapsed_1', 'pct_elapsed_2', 'pct_elapsed_3',
            'pct_elapsed_4', 'pct_elapsed_5']
    values = UDF.agg_cols(df=df, cols=cols, type_agg=TypeAgg.MEDIAN)
    values = [(1 - value)*100 for value in values]
    name_labels = 'Depth'
    name_values = 'Percentage of Elapsed Time Reduction'
    bar = Bar(labels=labels, values=values,
              name_labels=name_labels, name_values=name_values, is_pct=True)
    bar.show()


def show_correlation_explored_elapsed() -> None:
    """
    ========================================================================
     Show the correlation between explored and elapsed.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_explored_1'] = (1-df['pct_explored_1']) * 100
    df['pct_elapsed_1'] = (1-df['pct_elapsed_1']) * 100
    df = df[df['pct_explored_1'] >= -100]
    df = df[df['pct_explored_1'] <= 100]
    df = df[df['pct_elapsed_1'] >= -100]
    df = df[df['pct_elapsed_1'] <= 100]
    scatter = ScatterRegression(df=df,
                                col_x='pct_explored_1',
                                col_y='pct_elapsed_1',
                                name='Explored vs Elapsed')
    scatter.show()


def show_changed() -> None:
    """
    ========================================================================
     Show the changed.
    ========================================================================
    """
    df = pd.read_csv(csv_results)
    df['pct_changed_1'] = round(df['changed_1'] / df['nodes'] * 100, 2)
    df['pct_changed_2'] = round(df['changed_2'] / df['nodes'] * 100)
    df['pct_changed_3'] = round(df['changed_3'] / df['nodes'] * 100)
    df['pct_changed_4'] = round(df['changed_4'] / df['nodes'] * 100)
    df['pct_changed_5'] = round(df['changed_5'] / df['nodes'] * 100)
    df = df[['pct_changed_1', 'pct_changed_2', 'pct_changed_3',
             'pct_changed_4', 'pct_changed_5']]
    labels = ['1', '2', '3', '4', '5']
    cols = ['pct_changed_1', 'pct_changed_2', 'pct_changed_3',
            'pct_changed_4', 'pct_changed_5']
    values = UDF.agg_cols(df=df, cols=cols, type_agg=TypeAgg.MEDIAN)
    name_labels = 'Depth'
    name_values = 'Percentage of Changed Nodes from all Nodes'
    bar = Bar(labels=labels, values=values,
              name_labels=name_labels, name_values=name_values, is_pct=True)
    bar.show()


def show_pct_explored_nodes() -> None:
    """
    ========================================================================
     Show the percentage of explored nodes in distribution of number of
       nodes in the graph.
    ========================================================================
    """
    df = pd.read_csv(csv_results_temp)
    df = UDF.wide_to_long(df=df,
                          col_x='nodes',
                          col_y='depth',
                          cols_y=['pct_explored_1', 'pct_explored_2',
                                  'pct_explored_3', 'pct_explored_4',
                                  'pct_explored_5'],
                          col_val='pct_explored')
    pivot = UPivot.from_df(df=df,
                           col_x='nodes',
                           col_y='depth',
                           col_val='pct_explored',
                           mult_x=100000,
                           mult_y=1,
                           type_agg=UPivot.TypeAgg.MEAN)
    name = 'Percentage of explored nodes relatively to all nodes'
    heat_map = HeatMap(pivot=pivot, name=name)
    heat_map.show()


# union_csv()
# format_csv()
# show_pct_comparison()
# show_pct_comparison_to_zero()
show_pct_explored()
# show_pct_explored_only_better()
# show_pct_elapsed()
# show_correlation_explored_elapsed()
# show_changed()
# show_pct_explored_nodes()
 