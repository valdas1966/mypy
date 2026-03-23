from f_psl.pandas.csv import UCsv


path = 'f:\\temp\\2026\\03\\oracle\\results.csv'
metrics = ['elapsed', 'explored']

for metric in metrics:
    col_forward = f'{metric}_forward'
    col_backward = f'{metric}_ka_cached'
    cols = [col_forward, col_backward]
    col = f'{metric}_oracle'
    UCsv.add_col_agg(path=path, cols=cols, col=col, func=min)
