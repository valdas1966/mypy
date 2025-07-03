from f_ds.queues.i_1_fifo import QueueFIFO
from f_ds.old_grids.old_cell import Cell


def study_1():
    fifo = QueueFIFO()
    fifo.push(2)
    fifo.push(1)
    print(fifo)


def study_2():
    fifo = QueueFIFO()
    fifo.push(Cell(0, 2))
    fifo.push(Cell(1, 1))
    print(fifo)


study_2()
