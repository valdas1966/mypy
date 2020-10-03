from f_utils import u_pickle
from f_utils import u_list
from f_astar.c_astar import AStar

path_results = 'D:\\MyPy\\f_astar\\experiments\\results_astar_assymetry.csv'
pickle_maps = 'D:\\MyPy\\f_map\\maps\\maps.pickle'
maps = u_pickle.load(pickle_maps)

file = open(path_results, 'w')
titles = 'i,map,width,height,start,start_up,start_right,start_down,start_left,'
titles += 'goal,goal_up,goal_right,goal_down,goal_left,top,left,'
titles += 'distance,forward,backward\n'
file.write(titles)
file.close()
for m in maps:
    map = maps[m]
    for i in range(100):
        start, goal = map.get_random_idds(2)
        astar_forward = AStar(map.grid, start, goal)
        forward = len(astar_forward.closed)
        astar_backward = AStar(map.grid, goal, start)
        backward = len(astar_backward.closed)
        shape = u_list.to_str(map.shape)
        offsets_start = u_list.to_str(map.offsets(start))
        offsets_goal = u_list.to_str(map.offsets(goal))
        offsets_between = u_list.to_str(map.offsets(start, goal))
        distance = map.distance(start, goal)
        line = f'{i},{m},{shape},{start},{offsets_start},{goal},{offsets_goal},'
        line += f'{offsets_between},{distance},{forward},{backward}\n'
        file = open(path_results, 'a')
        file.write(line)
        file.close()
        print(m, i)
