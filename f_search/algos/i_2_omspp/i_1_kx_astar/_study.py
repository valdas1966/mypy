from f_search.algos.i_2_omspp import KxAStar

algo = KxAStar.Factory.without_obstacles()
algo._verbose = True
algo.run()
