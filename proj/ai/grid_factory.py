import numpy as np
from proj.ai.model.grid_blocks import GridBlocks


def gen_roomap(path, char_valid='.', rows_pass=4):
    rows = list()
    file = open(path, 'r')
    lines = file.readlines()[rows_pass:]
    for line in lines:
        row = line.split()
        row = [0 if x == char_valid else -1 for x in row]
        rows.append(row)
    file.close()
    ndarray = np.array(rows)
    grid = GridBlocks(rows=ndarray.shape[0], cols=ndarray.shape[1])
    grid.ndarray = ndarray
    return grid
