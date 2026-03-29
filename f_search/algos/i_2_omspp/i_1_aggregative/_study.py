from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative

algo = AStarAggregative.Factory.with_obstacles()
solution = algo.run()

data = algo._data
for i, state in enumerate(data.explored):
    g = data.dict_g.get(state)
    h_vec = data.dict_h.get(state)
    h_min = min(h_vec)
    f = g + h_min
    row, col = state.key.row, state.key.col
    print(f'{i+1}. ({row},{col})  g={g}  f={f}  h={h_vec}')
