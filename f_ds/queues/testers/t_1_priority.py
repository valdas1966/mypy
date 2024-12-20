import pytest
from f_ds.queues.i_1_priority import QueuePriority


@pytest.fixture
def ex() -> QueuePriority:
    q = QueuePriority[int]()
    q.push(item=2)
    q.push(item=1)
    return q


def test_push(ex):
    assert list(ex) == [1, 2]


def test_pop(ex):
    assert ex.pop() == 1
