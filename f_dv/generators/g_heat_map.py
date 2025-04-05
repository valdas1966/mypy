import pandas as pd
from f_dv.heat_map import HeatMap
from f_psl.pandas.u_pivot import UPivot


x = [1, 1, 1, 2, 2, 5, 5]
y = [1, 1, 2, 1, 2, 1, 2]
val = [10, 10, 20, 30, 40, 50, 60]

df = pd.DataFrame({'x': x, 'y': y, 'val': val})
pivot = UPivot.from_df(df=df, col_x='x', col_y='y', col_val='val')

heat_map = HeatMap(pivot=pivot, name='Heat Map')
heat_map.show()

