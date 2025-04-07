from f_file.i_1_csv import CSV
from f_psl.os.u_folder import UFolder
from f_psl.pandas.u_df import UDF, TypeAgg
from f_dv.i_1_bar import Bar
from f_dv.i_1_scatter import Scatter
import pandas as pd


cd = 'd'
folder = f'{cd}:\\temp\\boundary\\grands'
folder_results = f'{folder}\\results'
csv_results = f'{folder}\\results.csv'


def union_csv() -> None:
    """
    ========================================================================
     Union the csv files.
    ========================================================================
    """
    paths_from = UFolder.filepaths(path=folder_results)
    CSV.union(paths_from=paths_from, path_to=csv_results)


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
    values = [(1 - value)*100 for value in values]
    name_labels = 'Depth'
    name_values = 'Percentage of Exploration Reduction'
    bar = Bar(labels=labels, values=values,
              name_labels=name_labels, name_values=name_values, is_pct=True)
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
    # remiain only pct_explored_1 between -200 and 200
    df = df[df['pct_explored_1'] >= -50]
    df = df[df['pct_explored_1'] <= 50]
    df = df[df['pct_elapsed_1'] >= -50]
    df = df[df['pct_elapsed_1'] <= 50]
    scatter = Scatter(df=df,
                      col_x='pct_explored_1',
                      col_y='pct_elapsed_1',
                      name='Explored vs Elapsed')
    scatter.show()


# union_csv()
# show_pct_explored()
# show_pct_elapsed()
show_correlation_explored_elapsed()
