from f_map.c_map_rooms import MapRooms
from f_utils import u_random


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
    return list(maps)


maps = gen_maps(rows=10, cols=10, amount=10)
for map in maps:
    print(map.grid)
    print()
