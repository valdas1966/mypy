from f_search.algos import Dijkstra


algo = Dijkstra.Factory.without_obstacles()
algo._verbose = True
algo.run()
