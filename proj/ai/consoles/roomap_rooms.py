from f_utils import u_pickle
from proj.ai.model.point import Point


dir_results = 'D:\\Exp_RooMap\\'
pickle_grids = dir_results + 'grids.pickle'
pickle_start_goals = dir_results + 'start_goals.pickle'
csv_rooms = dir_results + 'rooms.csv'


def to_point_room(point, size_room):
    x = point.x // size_room
    y = point.y // size_room
    return Point(x, y)


grids = u_pickle.load(pickle_grids)
sg = u_pickle.load(pickle_start_goals)

file = open(csv_rooms, 'w')
file.write('map,experiment,distance\n')
for i, grid in enumerate(grids):
    for j, (start, goals) in enumerate(sg[i]):
        room_start = to_point_room(start, grid.size_room)
        room_goals = to_point_room(goals[0], grid.size_room)
        distance = room_start.distance(room_goals)
        file.write(f'{i},{j},{distance}\n')
file.close()
