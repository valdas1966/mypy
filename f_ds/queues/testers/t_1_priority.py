from f_ds.queues.i_1_priority import QueuePriority


def test_priority():
    q = QueuePriority()
    q.push(item=2)
    q.push(item=1)
    # 1 is the Min-Item
    assert q.pop() == 1
