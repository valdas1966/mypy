import pandas as pd
from f_dv.heat_map import HeatMap


x = [1, 1, 1, 2, 2, 5, 5]
y = [1, 1, 2, 1, 2, 1, 2]
volume = [10, 10, 20, 30, 40, 50, 60]

df = pd.DataFrame({'x': x, 'y': y, 'volume': volume})

heat_map = HeatMap(df=df, name='Heat Map')
heat_map.show()

