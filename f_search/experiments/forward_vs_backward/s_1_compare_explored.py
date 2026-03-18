from f_psl.pandas.csv import UCsv


"""
===============================================================================
 Compare Explored Nodes between Forward and Backward Searches.
-------------------------------------------------------------------------------
 Input:  CSV with 'explored_forward' and 'explored_backward' columns.
 Output: Same CSV with added 'min', 'pct', and 'oracle' columns.
===============================================================================
"""

# path = '/Users/eyalberkovich/temp/2026/03/Forward and Backward/analytics.csv'
path = 'f:\\temp\\2026\\03\\Forward vs Backward\\results.csv'

col_forward = 'explored_forward'
col_backward = 'explored_backward'

UCsv.add_comparing_cols(path=path, col_a=col_forward, col_b=col_backward)
