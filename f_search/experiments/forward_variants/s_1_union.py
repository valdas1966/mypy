from f_psl.pandas.csv import UCsv

path_1 = 'f:\\temp\\2026\\03\\incremental\\results.csv'
path_2 = 'f:\\temp\\2026\\03\\incremental 200\\results.csv'
path_output = 'f:\\temp\\2026\\03\\forward variants\\results.csv'

UCsv.union(path_1=path_1, path_2=path_2, path_output=path_output)
