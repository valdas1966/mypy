from f_psl.pandas.csv import UCsv


"""
===============================================================================
 Group Explored Nodes by K (number of goals).
-------------------------------------------------------------------------------
 Input:  CSV with 'explored_forward', 'explored_backward', 'oracle', and 'k'.
 Output: CSV grouped by 'k' with mean aggregation.
===============================================================================
"""

#folder = '/Users/eyalberkovich/temp/2026/03/Forward and Backward'
#path_input = f'{folder}/analytics.csv'
#path_output = f'{folder}/grouped_by_k.csv'
folder = 'f:\\temp\\2026\\03\\Forward vs Backward'
path_input = f'{folder}\\results.csv'
path_output = f'{folder}\\grouped_by_k.csv'

col_group = 'k'
cols_value = ['explored_forward', 'explored_backward', 'oracle']

UCsv.group(path_input=path_input,
           path_output=path_output,
           col_a=col_group,
           col_b=cols_value,
           agg='mean')
