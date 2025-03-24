from f_ds.queues.generators.g_1_list import GenQueueList


def test_push() -> None:
    """
    ========================================================================
     Test the Push-Method.
    ========================================================================
    """
    q = GenQueueList.empty()
    assert q.to_iterable() == []
    q.push(1)
    assert q.to_iterable() == [1]


def test_pop() -> None:
    """
    ========================================================================
     Test the Pop-Method.
    ========================================================================
    """ 
    q = GenQueueList.trio()
    q.push(0)
    assert q.pop() == 0
    assert q.to_iterable() == [1, 2, 3]
    assert q.pop() == 1
    assert q.to_iterable() == [2, 3]
    assert q.pop() == 2
    assert q.to_iterable() == [3]
    assert q.pop() == 3
    assert q.to_iterable() == []


def test_peek() -> None:
    """
    ========================================================================
     Test the Peek-Method.
    ========================================================================
    """ 
    q = GenQueueList.trio()
    assert q.peek() == 1
    assert q.to_iterable() == [1, 2, 3]


def test_update() -> None:
    """
    ========================================================================
     Test the Update-Method.
    ========================================================================
    """ 
    q = GenQueueList.trio()
    q.push(0)
    q.update()
    assert q.to_iterable() == [0, 1, 2, 3]
