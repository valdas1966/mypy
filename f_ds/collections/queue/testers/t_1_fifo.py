from f_ds.collections.queue.i_1_fifo import QueueFIFO


def test_fifo():
    q = QueueFIFO()
    q.push(element=2)
    q.push(element=1)
    assert q.pop() == 2
