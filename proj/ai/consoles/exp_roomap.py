from f_utils import u_file
from f_utils import u_pickle
from f_utils.c_timer import Timer
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks_roomap import GridBlocksRooMap
from proj.ai.algo.kastar_projection import KAStarProjection
from proj.ai.algo.kastar_backward import KAStarBackward
from proj.ai.algo.kastar_bi import KAStarBi

dir_results = 'D:\\Exp_RooMap\\'
pickle_grids = dir_results + 'grids.pickle'
pickle_start_goals = dir_results + 'start_goals.pickle'
pickle_forward = dir_results + 'forward.pickle'
pickle_backward = dir_results + 'backward.pickle'
pickle_bi = dir_results + 'bi.pickle'


def get_size_room(path):
    if path[1].isdigit():
        return int(path[:2])
    return int(path[0])


def create_grids():
    dir_maps = 'D:\\Maps'
    grids = list()
    for filename in u_file.get_files_names(dir_maps):
        path = f'{dir_maps}\\{filename}'
        size_room = get_size_room(filename)
        grid = GridBlocksRooMap(path, size_room=size_room)
        grids.append(grid)
    u_pickle.dump(grids, pickle_grids)


def create_start_goals():
    start_goals = list()
    grids = u_pickle.load(pickle_grids)
    for grid in grids:
        epochs = list()
        for i in range(10):
            point_room_start, point_room_goals = grid.random_rooms(2)
            room_start = grid.get_room(point_room_start)
            start = room_start.points_random(amount=1)[0]
            start = grid.to_actual_point(start, point_room_start)
            room_goals = grid.get_room(point_room_goals)
            goals = room_goals.points_random(amount=10)
            goals = [grid.to_actual_point(goal, point_room_goals) for goal in
                     goals]
            epochs.append((start, goals))
        start_goals.append(epochs)
    u_pickle.dump(start_goals, pickle_start_goals)


def create_forward():
    li_forward = list()
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    for i, grid in enumerate(grids):
        epochs = list()
        for j, sg in enumerate(start_goals[i]):
            print(i, j)
            start, goals = sg
            kastar = KAStarProjection(grid, start, goals)
            epochs.append(kastar)
        li_forward.append(epochs)
    u_pickle.dump(li_forward, pickle_forward)


def create_backward():
    timer = Timer()
    li_backward = list()
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    for i, grid in enumerate(grids):
        epochs = list()
        for j, sg in enumerate(start_goals[i]):
            start, goals = sg
            kastar = KAStarBackward(grid, start, goals)
            epochs.append(kastar)
            elapsed = timer.elapsed()
            print(i, j, elapsed)
        li_backward.append(epochs)
    u_pickle.dump(li_backward, pickle_backward)


def create_bi():
    timer = Timer()
    li_bi = list()
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    for i, grid in enumerate(grids):
        epochs = list()
        for j, sg in enumerate(start_goals[i]):
            start, goals = sg
            kastar = KAStarBi(grid, start, goals)
            epochs.append(kastar)
            elapsed = timer.elapsed()
            print(i, j, elapsed)
        li_bi.append(epochs)
    u_pickle.dump(li_bi, pickle_bi)


def create_report():
    li_forward = u_pickle.load(pickle_forward)
    li_backward = u_pickle.load(pickle_backward)
    li_bi = u_pickle.load(pickle_bi)
    csv_report = dir_results + 'report.csv'
    file = open(csv_report, 'w')
    file.write('map,experiment,forward,backward,bidirectional,oracle\n')
    for i in range(40):
        for j in range(10):
            forward = len(li_forward[i][j].closed)
            backward = len(li_backward[i][j].closed)
            bi = len(li_bi[i][j].closed)
            oracle = min(forward, backward, bi)
            file.write(f'{i},{j},{forward},{backward},{bi},{oracle}\n')
    file.close()


# create_grids()
# create_start_goals()
# create_forward()
# create_backward()
# create_bi()
# create_report()
