"""
============================================================================
 Download results_unified.csv from Drive, group by [k] into
 separate CSV files, and upload them back to Drive.
============================================================================
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', '..', '..', '..')))

from f_psl.pandas import UCsv
from f_google.services.drive import Drive

PATH_DRIVE_INPUT = '2026/04/Experiments/OMSPP/results_unified.csv'
PATH_DRIVE_FOLDER = '2026/04/Experiments/OMSPP'
_tmp = os.environ.get('TEMP', '/tmp')
PATH_TMP_INPUT = os.path.join(_tmp, 'results_unified.csv')

groups = {
    'elapsed':    ['elapsed_inc', 'elapsed_agg'],
    'explored':   ['explored_inc', 'explored_agg'],
    'discovered': ['discovered_inc', 'discovered_agg'],
    'h_calc':     ['h_calcs_inc', 'h_calcs_agg'],
    'surely':     ['surely_inc', 'surely_agg'],
    'borderline': ['border_inc', 'border_agg'],
}

drive = Drive.Factory.valdas()
drive.download(path_src=PATH_DRIVE_INPUT,
               path_dest=PATH_TMP_INPUT)
print(f'Downloaded {PATH_DRIVE_INPUT}')

for name, cols in groups.items():
    path_tmp = os.path.join(_tmp, f'{name}.csv')
    UCsv.group(path_input=PATH_TMP_INPUT,
               path_output=path_tmp,
               col_a='k',
               col_b=cols,
               agg='mean')
    path_drive = f'{PATH_DRIVE_FOLDER}/{name}.csv'
    drive.upload(path_src=path_tmp, path_dest=path_drive)
    print(f'Uploaded {name}.csv')
print('Done')
