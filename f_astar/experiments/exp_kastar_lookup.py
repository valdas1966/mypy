from f_utils import u_pickle
from f_astar.c_astar import AStar
from f_astar.c_astar_lookup import AStarLookup
from f_const.directions import Directions

path_results = 'G:\\MyPy\\f_astar\\experiments\\results_kastar_lookup_5.csv'
path_astars = 'G:\\MyPy\\astars_5\\'
pickle_maps = 'G:\\MyPy\\f_map\\maps\\maps.pickle'
maps = u_pickle.load(pickle_maps)

file = open(path_results, 'w')
titles = 'map,i,start,goal_near,goal_far,closed,forward,backward,d,rows,cols,'
titles += 'row_start,col_start,row_goal_near,col_goal_near,row_goal_far,'
titles += 'col_goal_far,distance_start_goal_near,distance_start_goal_far,'
titles += 'distance_between_goals,f_goal_near,nearest_closed_up,'
titles += 'nearest_closed_right,nearest_closed_down,nearest_closed_left\n'
file.write(titles)
file.close()
for m in maps:
    map = maps[m]
    for i in range(100):
        start, goal_near, goal_far = [None] * 3
        expanded_near, f_goal_near, forward = [None] * 3
        closed_1, set_path_new = set(), set()
        found_solution = False
        counter = 0
        while not found_solution:
            start, goal_1, goal_2 = map.get_random_idds(3)
            goals = {goal_1, goal_2}
            goal_near = map.nearest(start, goals)
            goal_far = goal_1 if goal_2 == goal_near else goal_2
            astar = AStar(map.grid, start, goal_near)
            astar.run()
            if not astar.best:
                print('not found solution forward near')
                continue
            expanded_near = len(astar.closed)
            f_goal_near = astar.best.f
            path_astar = path_astars + f'{m}_{str(i).zfill(3)}.pickle'
            u_pickle.dump(astar, path_astar)
            lookup = astar.closed.copy()
            closed_1 = {node.idd for node in astar.closed}
            astar.run(goal_far)
            if not astar.best:
                print('not found solution forward far')
                continue
            set_path_new = set(astar.get_path())
            forward = len(astar.closed) - expanded_near
            astar_lookup = AStarLookup(map.grid, goal_far, start, closed=lookup)
            astar_lookup.run()
            found_solution = astar_lookup.is_found
            if not found_solution:
                print('not found solution backward')
        d = len(set_path_new - closed_1)
        backward = len(astar_lookup.closed)
        row_start, col_start = map.to_row_col(start)
        row_goal_near, col_goal_near = map.to_row_col(goal_near)
        row_goal_far, col_goal_far = map.to_row_col(goal_far)
        distance_start_goal_near = map.distance(start, goal_near)
        distance_start_goal_far = map.distance(start, goal_far)
        distance_between_goals = map.distance(goal_near, goal_far)
        idds_closed = {node.idd for node in lookup}
        nearest_closed = map.nearest_closed(goal_far, idds_closed)
        line = f'{m},{i},{start},{goal_near},{goal_far},{expanded_near},'
        line += f'{forward},{backward},{d},{map.rows},{map.cols},'
        line += f'{row_start},{col_start},{row_goal_near},{col_goal_near},'
        line += f'{row_goal_far},{col_goal_far},{distance_start_goal_near},'
        line += f'{distance_start_goal_far},'
        line += f'{distance_between_goals},{f_goal_near},'
        line += f'{nearest_closed[Directions.UP]},'
        line += f'{nearest_closed[Directions.RIGHT]},'
        line += f'{nearest_closed[Directions.DOWN]},'
        line += f'{nearest_closed[Directions.LEFT]}\n'
        file = open(path_results, 'a')
        file.write(line)
        file.close()
        print(m, str(i).zfill(3))
