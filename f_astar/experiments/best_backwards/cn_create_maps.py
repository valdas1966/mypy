from f_map.c_map import Map
from f_utils import u_pickle
from f_astar.c_astar import AStar
from f_astar.c_astar_lookup import AStarLookup


dir_maps = 'G:\\MyPy\\f_astar\\experiments\\best_backwards\\Maps\\'
pickle_maps = dir_maps + 'maps.pickle'
pickle_start_goals = dir_maps + 'start_goals.pickle'
pickle_forward = dir_maps + 'forward.pickle'
pickle_backward = dir_maps + 'backward.pickle'
csv_report = dir_maps + 'report.csv'


def create_maps(amount, rows, cols, obstacles):
    """
    ============================================================================
     Description: Create 1000 Randomized Maps 10x10 with 30% obstacles.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. amount : int (Amount of Maps).
        2. rows : int (Amount of Rows in the Map).
        3. cols: int (Amount of Columns in the Map).
        4. obstacles : int (Percent of Obstacles in the Map).
    ============================================================================
     Pickle:
    ----------------------------------------------------------------------------
        1. List of Maps.
    ============================================================================
    """
    maps = list()
    for i in range(amount):
        map = Map(rows=rows, cols=cols, obstacles=obstacles)
        maps.append(map)
    u_pickle.dump(maps, pickle_maps)


def create_start_goals(amount, verbose=True):
    """
    ============================================================================
     Description: Create 1000 different Start and Goals epochs for each Map.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. amount : int (Amount of Epochs).
    ============================================================================
     Pickle:
    ----------------------------------------------------------------------------
        1. List (maps) of List (start and goals) of Dict {start, goal_near,
                                                            goal_far}.
    ============================================================================
    """
    maps = u_pickle.load(pickle_maps)
    start_goals = list()
    for e, map in enumerate(maps):
        epochs = list()
        for i in range(amount):
            start, goal_1, goal_2 = map.get_random_idds(3)
            goal_near = map.nearest(start, [goal_1, goal_2])
            goal_far = ({goal_1, goal_2} - {goal_near}).pop()
            d = {'start': start, 'goal_near': goal_near, 'goal_far': goal_far}
            epochs.append(d)
        start_goals.append(epochs)
        if verbose:
            print(f'Start Goals {e}')
    u_pickle.dump(start_goals, pickle_start_goals)


def run_forward():
    """
    ============================================================================
     Description: Run Forward KA* to near and far Goals.
    ============================================================================
     Pickle: List (maps) of List (ka*) of Dict {closed_near: set of nodes,
                                                closed_far: set of nodes}.
    ============================================================================
    """
    maps = u_pickle.load(pickle_maps)
    start_goals = u_pickle.load(pickle_start_goals)
    forward = list()
    for i in range(len(maps)):
        map = maps[i]
        epoch = list()
        for j in range(len(start_goals)):
            sg = start_goals[i][j]
            start = sg['start']
            goal_near = sg['goal_near']
            goal_far = sg['goal_far']
            astar = AStar(map.grid, start, goal_near)
            astar.run()
            if not astar.best:
                epoch.append(None)
                continue
            closed_near = astar.closed.copy()
            astar.run(goal_far)
            if not astar.best:
                epoch.append(None)
                continue
            closed_far = astar.closed - closed_near
            ans = {'closed_near': closed_near, 'closed_far': closed_far}
            epoch.append(ans)
        forward.append(epoch)
        print(f'Forward {i}')
    u_pickle.dump(forward, pickle_forward)


def run_backward():
    """
    ============================================================================
     Description: Run Backward A* to the Start from the far Goal
                    (using closed_near from the forward search).
    ============================================================================
     Pickle: List (Maps) of List (Back A*) of Closed Backward (set of nodes).
    ============================================================================
    """
    maps = u_pickle.load(pickle_maps)
    start_goals = u_pickle.load(pickle_start_goals)
    forward = u_pickle.load(pickle_forward)
    backward = list()
    for i in range(len(maps)):
        map = maps[i]
        epoch = list()
        for j in range(len(start_goals)):
            sg = start_goals[i][j]
            start = sg['start']
            goal_far = sg['goal_far']
            fw = forward[i][j]
            if not fw:
                epoch.append(None)
                continue
            closed_near = fw['closed_near']
            astar_lookup = AStarLookup(grid=map.grid, start=goal_far,
                                       goal=start, closed=closed_near)
            astar_lookup.run()
            epoch.append(astar_lookup.closed)
        backward.append(epoch)
        print(f'Backward {i}')
    u_pickle.dump(backward, pickle_backward)


def run_report():
    maps = u_pickle.load(pickle_maps)
    start_goals = u_pickle.load(pickle_start_goals)
    forward = u_pickle.load(pickle_forward)
    backward = u_pickle.load(pickle_backward)
    file = open(csv_report, 'w')
    file.write('Map, Epoch, Start, Goal Near, Goal Far, Distance Near, '
               'Distance Far, Distance Goals, Lookup, Ratio, Forward, Backward,'
               'Delta\n')
    for i in range(len(maps)):
        map = maps[i]
        for j in range(len(start_goals)):
            sg = start_goals[i][j]
            start = sg['start']
            goal_near = sg['goal_near']
            goal_far = sg['goal_far']
            distance_near = map.distance(start, goal_near)
            distance_far = map.distance(start, goal_far)
            distance_goals = map.distance(goal_near, goal_far)
            fw = forward[i][j]
            if not fw:
                continue
            closed_near = len(fw['closed_near'])
            closed_far = len(fw['closed_far'])
            closed_back = len(backward[i][j])
            ratio_near = round(distance_near / closed_near * 100, 0)
            file.write(f'{i}, {j}, {start}, {goal_near}, {goal_far},'
                       f'{distance_near}, {distance_far}, {distance_goals}'
                       f',{closed_near}, {ratio_near}, {closed_far},'
                       f' {closed_back}, {closed_far-closed_back}\n')
        print(f'Report {i}')
    file.close()


# 1. Create 1000 Randomized Maps 10x10 with 30% obstacles.
# create_maps(amount=1000, rows=10, cols=10, obstacles=30)

# 2. Create 1000 Epochs of different Start and Goals for each Map.
# create_start_goals(amount=1000)

# 3. Run 1000*100 KA*
# run_forward()

# 4. Run 1000*100 Backward A* (using forward closed_near as lookup).
# run_backward()

# 5. Report Results
run_report()
