from collections import defaultdict
from f_utils import u_pickle
from f_psl.os.u_path import UPath
from f_psl.os.u_folder import UFolder
from f_ds.grids.grid.map import GridMap as Grid


path = 'g:\\paper\\maps'
filepaths = UFolder.filepaths(path=path, recursive=True)

grids = defaultdict(dict[str, list[Grid]])
for filepath in filepaths:
    domain = UPath.last_folder(path=filepath)
    name = UPath.filename(path=filepath, with_domain=False)
    grid = Grid.From.file_map(path=filepath, name=name)
    grids[domain][name] = grid
    print(f'{domain},{name}, {grid.rows}x{grid.cols}, {len(grid)}')

u_pickle.dump(obj=grids, path='g:\\paper\\grids.pkl')
