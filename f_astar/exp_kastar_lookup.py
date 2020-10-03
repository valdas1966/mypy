from f_astar.c_kastar_lookup import KAStarLookup
from f_astar.c_kastar import KAStar
from f_grid import u_grid
from f_grid import u_gidd
from f_grid import u_create

path_results = 'G:\\MyPy\\f_astar\\results_kastar_lookup.csv'
path_map = 'G:\\MyPy\\f_astar\\ost000a.map'
grid = u_create.from_map(path_map)
pairs = u_gidd.gen_random_pairs(grid, 100, 1000)
print(len(pairs))

file = open(path_results, 'a')
file.write('start, goal_1, goal_2, distance_start_goal_1,'
           ' distance_start_goal_2,'
           ' distance_between_goals, expanded_goal_1,'
           ' expanded_kastar, expanded_kastar_lookup\n')
file.close()
for i, pair in enumerate(pairs):
    print(i)
    start, goal_1 = pair
    goal_2 = u_gidd.get_random_idds(grid, goal_1, 10, 1).pop()
    goals = {goal_1, goal_2}
    kastar = KAStar(grid, start, goals)
    kastar.run()
    kastar_lookup = KAStarLookup(grid, start, goals)
    kastar_lookup.run()

    distance_start_goal_1 = u_grid.manhattan_distance(grid, start, goal_1)
    distance_start_goal_2 = u_grid.manhattan_distance(grid, start, goal_2)
    distance_between_goals = u_grid.manhattan_distance(grid, goal_1, goal_2)
    expanded_goal_1 = kastar_lookup.expanded_forward
    expanded_kastar = len(kastar.closed)
    expanded_kastar_lookup = kastar_lookup.expanded_nodes
    file = open(path_results, 'a')
    line_format = '{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'
    line = line_format.format(start, goal_1, goal_2, distance_start_goal_1,
                              distance_start_goal_2, distance_between_goals,
                              expanded_goal_1, expanded_kastar,
                              expanded_kastar_lookup)
    file.write(line)
    file.close()
