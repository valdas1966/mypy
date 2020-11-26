from proj.ai.model.grid_blocks import GridBlocks


def gen_roomap(path, point_accessible='.'):
    lines = list()
    file = open(path, 'r')
    for line in file.readlines():
        line.append()
    file.close()