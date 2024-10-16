from f_ds.queues.i_1_fifo import QueueFIFO
from f_ds.queues.i_1_priority import QueuePriority
from f_graph.data.i_2_one_to_one import DataOneToOne


def test_fifo():
    data = DataOneToOne(type_queue=QueueFIFO)
    data.generated.push(2)
    data.generated.push(1)
    assert data.generated.pop() == 2


def test_priority():
    data = DataOneToOne(type_queue=QueuePriority)
    data.generated.push(2)
    data.generated.push(1)
    assert data.generated.pop() == 1
