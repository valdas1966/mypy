from f_psl.pandas import UCsv

path = 'f:\\temp\\2026\\03\\oracle\\results.csv'

cols = ['h_start', 'h_goals']

for col in cols:
    UCsv.add_col_bins(path=path, col=col, n=10)
