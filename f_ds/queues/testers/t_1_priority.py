from f_ds.queues.i_1_priority import QueuePriority
from f_ds.queues.generators.g_1_priority import GenPriorityQueue, Item
import pytest


@pytest.fixture
def queue() -> QueuePriority[Item]:
    return GenPriorityQueue.gen_2()


def test_pop(queue: QueuePriority[Item]) -> None:
    items = list(queue)
    item = queue.pop()
    assert item == items[0]


def test_push(queue: QueuePriority[Item]) -> None:
    queue.push(item=Item(val=3))
    assert list(queue) == [Item(val=1), Item(val=2), Item(val=3)]


def test_peek(queue: QueuePriority[Item]) -> None:
    assert queue.peek() == Item(val=1)
    assert len(queue) == 2


def test_undo_pop(queue: QueuePriority[Item]) -> None:
    item = queue.pop()
    queue.undo_pop(item=item)
    assert list(queue) == [Item(val=1), Item(val=2)]


def test_update(queue: QueuePriority[Item]) -> None:
    items = list(queue)
    items[0].val = 20
    items[1].val = 10
    queue.update()
    assert list(queue) == [Item(val=10), Item(val=20)]
