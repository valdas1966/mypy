from f_psl.pandas.csv import UCsv


def group_by(key: str, metric: str) -> None:
    folder = 'f:\\temp\\2026\\03\\oracle'
    csv_results = f'{folder}\\results.csv'
    csv_group_by = f'{folder}\\{metric}_by_{key}.csv'
    col_b = [f'{metric}_kxa', f'{metric}_ka_cached', f'{metric}_ka_bounded', f'{metric}_forward', f'{metric}_oracle']
    UCsv.group(path_input=csv_results,
               path_output=csv_group_by,
               col_a=key,
               col_b=col_b,
               agg='mean')

keys = ['k', 'domain', 'binned_h_start', 'binned_h_goals']
metrics = ['explored', 'elapsed']

for key in keys:
    for metric in metrics:
        group_by(key=key, metric=metric)
