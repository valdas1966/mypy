import pytest
from f_ds.old_queues.i_1_fifo import QueueFIFO


@pytest.fixture
def ex() -> QueueFIFO:
    q = QueueFIFO()
    q.push(item=2)
    q.push(item=1)
    return q


def test_push(ex):
    assert list(ex) == [2, 1]


def test_pop(ex):
    assert ex.pop() == 2
