from f_utils import u_pickle
from f_excel.c_excel import Excel
from f_map.c_map_color import MapColor

dir_data = r'D:\\Temp\\'

pickle_maps = dir_data + 'maps.pickle'
pickle_start_goals = dir_data + 'start_goals.pickle'
pickle_forward = dir_data + 'forward.pickle'
pickle_backward = dir_data + 'backward.pickle'
pickle_maps_color = dir_data + 'maps_color.pickle'


def dump():
    maps = u_pickle.load(pickle_maps)
    start_goals = u_pickle.load(pickle_start_goals)
    forward = u_pickle.load(pickle_forward)
    backward = u_pickle.load(pickle_backward)
    maps_color = list()
    for i in range(len(maps)):
        row = list()
        map = maps[i]
        for j in range(len(start_goals)):
            sg = start_goals[i][j]
            fore = forward[i][j]
            if not fore:
                row.append(None)
                continue
            back = backward[i][j]
            map_color = MapColor(map, sg, fore, back)
            row.append(map_color)
        maps_color.append(row)
        print(i)
    u_pickle.dump(maps_color, pickle_maps_color)


excel_temp = dir_data + 'temp_2.xlsx'

maps_color = u_pickle.load(pickle_maps_color)
map_color = maps_color[1][1]

xl = Excel(excel_temp)
map_color.draw(xl, row_start=3, col_start=3)
xl.close()
