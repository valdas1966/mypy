from f_ds.queues.i_1_fifo import QueueFIFO


def test_fifo():
    q = QueueFIFO()
    q.push(item=2)
    q.push(item=1)
    # Item [2] was inserted first
    assert q.pop() == 2
