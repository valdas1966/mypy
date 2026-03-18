from f_psl.pandas.csv import UCsv


"""
===============================================================================
 Compare Explored Nodes between Forward and Backward Searches.
-------------------------------------------------------------------------------
 Input:  CSV with 'explored_forward' and 'explored_backward' columns.
 Output: Same CSV with added 'min', 'pct', and 'oracle' columns.
===============================================================================
"""

path = '/Users/eyalberkovich/temp/2026/03/Forward and Backward/results.csv'
# path = 'f:\\temp\\2026\\03\\Forward vs Backward\\results.csv'

metric = 'explored'
col_forward = f'{metric}_forward'
col_backward = f'{metric}_backward'
cols = [col_forward, col_backward]
col = f'{metric}_oracle'

UCsv.add_col_agg(path=path, cols=cols, col=col, func=min)
