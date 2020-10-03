from f_utils import u_pickle
from f_utils import u_file
from f_map.c_map import Map


def create_maps():
    """
    ============================================================================
     Description: Create Pickle of Dict of Maps in format {FileName: Grid}.
    ============================================================================
    """
    path_dir = 'D:\\MyPy\\f_map\\maps'
    path_pickle = path_dir + '\\maps.pickle'
    maps = dict()
    paths = u_file.get_files_names(path_dir)
    for i, path in enumerate(paths):
        if i == 114:
            continue
        path = path_dir + '\\' + path
        map = Map(path=path)
        filename = u_file.get_filename(path)
        maps[filename] = map
        print(f'{i+1}/{len(paths)}')
    u_pickle.dump(maps, path_pickle)


create_maps()