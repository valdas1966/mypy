"""
============================================================================
 Group merged.csv by [k] into separate CSV files.
============================================================================
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', '..', '..', '..')))

from f_psl.pandas import UCsv

folder = 'f:\\temp\\2026\\04\\closed categories'
path_input = f'{folder}\\merged.csv'

groups = {
    'elapsed':    ['elapsed_inc', 'elapsed_agg'],
    'explored':   ['explored_inc', 'explored_agg'],
    'h_calc':     ['cnt_h_inc', 'cnt_h_agg'],
    'surely':     ['surely_inc', 'surely_agg'],
    'borderline': ['border_inc', 'border_agg'],
}

for name, cols in groups.items():
    path_output = f'{folder}\\{name}.csv'
    UCsv.group(path_input=path_input,
               path_output=path_output,
               col_a='k',
               col_b=cols,
               agg='mean')
    print(f'{name}.csv')
print('Done')
