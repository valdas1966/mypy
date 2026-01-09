from f_search.algos.i_2_omspp import AStarRepeated

algo = AStarRepeated.Factory.with_obstacles()
algo._verbose = True
algo.run()
