import pandas as pd

path_csv = 'D:\\MyPy\\f_ds\\testers\\df column dtype.csv'

df = pd.read_csv(path_csv)

for i, str(v) in df.dtypes.items():
    print(type(i), type(v))