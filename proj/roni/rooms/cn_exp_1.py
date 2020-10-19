from f_map.c_map_rooms import MapRooms
from f_utils import u_random
from f_utils import u_pickle
from f_excel.c_excel_map import ExcelMap
import random


dir_storage = 'D:\\Temp\\Rooms'
pickle_maps = dir_storage + '\\maps.pickle'
pickle_start_goals = dir_storage + '\\start_goals.pickle'
excel_maps = dir_storage + '\\maps.xlsx'


def gen_maps(rows, cols, amount):
    maps = set()
    for i in range(amount):
        is_valid = False
        while not is_valid:
            # Try Set Blocks
            row_block = u_random.get_random_int(2, 7)
            col_block = u_random.get_random_int(2, 7)
            if row_block + col_block < 9:
                continue
            # Set Door
            row_door, col_door = None, None
            is_row = u_random.get_random_int(0, 1)
            if is_row:
                row_door = u_random.get_random_int(0, row_block-1)
            else:
                col_door = u_random.get_random_int(0, col_block-1)
            # Try Set Map
            map_rooms = MapRooms(rows, row_block, col_block,
                                 cols, row_door, col_door)
            if map_rooms in maps:
                continue
            maps.add(map_rooms)
            is_valid = True
    u_pickle(list(maps), pickle_maps)


def draw_maps():
    row_current = 2
    rows_delta = 14
    col_start = 2
    maps = u_pickle.load(pickle_maps)
    xl_map = ExcelMap(excel_maps)
    for i, map in enumerate(maps):
        map.draw_excel(xl_map=xl_map, row_start=row_current,
                       col_start=col_start, title=f'Map {str(i).zfill(2)}',
                       with_numbers=True)
        row_current += rows_delta
    xl_map.close()


def gen_start_goals():
    """
    ============================================================================
     Description: Generate Random Start and Goals Nodes.
    ============================================================================
     Pickle: List (100) of List (25*2*3) of Tuple (Point, List of Points).
    ============================================================================
    """
    maps = u_pickle.load(pickle_maps)
    start_goals_all = list()
    for i, map in enumerate(maps):
        start_goals_map = list()
        for j in range(25):
            left = map.get_left_points()
            right = map.get_right_points()
            # Start in Left Room
            random.shuffle(left)
            random.shuffle(right)
            start = left[0]
            for k in [2, 3, 5]:
                goals = right[:k]
                start_goals_map.append((start, goals))
                print(i, j, k, 'left')
            # Start in Right Room
            random.shuffle(left)
            random.shuffle(right)
            start = right[0]
            for k in [2, 3, 5]:
                goals = left[:k]
                start_goals_map.append((start, goals))
                print(i, j, k, 'right')
        start_goals_all.append(start_goals_map)
        u_pickle.dump(start_goals_all, pickle_start_goals)


# gen_maps(rows=10, cols=10, amount=100)
# draw_maps()
# gen_start_goals()
