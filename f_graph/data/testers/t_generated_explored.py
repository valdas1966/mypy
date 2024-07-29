from f_ds.queues.i_1_fifo import QueueFIFO
from f_graph.data.generated_explored import DataGeneratedExplored


def test():
    data = DataGeneratedExplored[int](type_queue=QueueFIFO)
    data.generated.push(1)
    assert data.generated.pop() == 1

