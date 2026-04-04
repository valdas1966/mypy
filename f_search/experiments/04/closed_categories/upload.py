"""
============================================================================
 Upload CSV files (merged + grouped) to Google Drive.
============================================================================
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', '..', '..', '..')))

from f_google.services.drive import Drive

folder_local = 'f:\\temp\\2026\\04\\closed categories'
folder_drive = '2026/04/experiments/omspp'

files = ['merged.csv',
         'elapsed.csv',
         'explored.csv',
         'h_calc.csv',
         'surely.csv',
         'borderline.csv']

drive = Drive.Factory.valdas()
for file in files:
    path_src = f'{folder_local}\\{file}'
    path_dest = f'{folder_drive}/{file}'
    drive.upload(path_src=path_src, path_dest=path_dest)
    print(f'Uploaded {file}')
print('Done')
