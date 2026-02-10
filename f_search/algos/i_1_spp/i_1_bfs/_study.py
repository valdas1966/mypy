from f_search.algos.i_1_spp.i_1_bfs import BFS


bfs = BFS.Factory.without_obstacles_with_cell_00()
solution = bfs.run()
grid = bfs.problem.grid
cells_explored = {state.key for state in bfs._data.explored}
print(cells_explored)
