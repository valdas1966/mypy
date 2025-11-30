from f_search.algos.i_2_omspp import KxAStar

algo = KxAStar.Factory.with_obstacles()
algo._verbose = True
algo.run()
