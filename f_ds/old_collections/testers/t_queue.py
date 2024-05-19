from f_data_structure.collections.i_2_queue_fifo import QueueFIFO


def test_push():
    """
    ============================================================================
     1. Test the Queue is Empty after Init.
     2. Test the Queue is not Empty after Push.
    ============================================================================
    """
    q = QueueFIFO()
    assert not q
    q.push(1)
    assert q


def test_pop():
    """
    ============================================================================
     1. Test validity of Pop-Element.
     2. Test the Queue is empty after Pop.
    ============================================================================
    """
    q = QueueFIFO()
    q.push(1)
    q.push(2)
    assert q.pop() == 1
    assert q.pop() == 2
    assert not q


def test_elements():
    q = QueueFIFO()
    q.push(1)
    q.push(2)
    assert q.elements() == [1, 2]


def test_contains():
    q = QueueFIFO()
    q.push(1)
    assert 1 in q
