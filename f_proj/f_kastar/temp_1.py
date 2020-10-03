from f_utils import u_pickle
from f_ds import u_fs


pickle_df = 'D:\\MyPy\\f_astar\\experiments\\df.pickle'

df = u_pickle.load(pickle_df)
print(len(df.columns))
for t in (1, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9):
    print(t, len(u_fs.drop_correlated_features(df, t).columns))

