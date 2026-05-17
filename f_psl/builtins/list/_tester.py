from f_psl.builtins.list import UList


def test_sliding_windows() -> None:
    """
    ========================================================================
     Test the sliding_windows() method across:
      * the canonical example,
      * size 1 (singletons),
      * size equal to the list length (single window),
      * size larger than the list length (empty result),
      * empty list,
      * a longer list with size 3.
    ========================================================================
    """
    # Canonical example
    li = [1, 2, 3]
    size = 2
    actual = UList.sliding_windows(li=li, size=size)
    expected = [[1, 2], [2, 3]]
    assert actual == expected

    # Size 1
    li = [1, 2, 3]
    size = 1
    actual = UList.sliding_windows(li=li, size=size)
    expected = [[1], [2], [3]]
    assert actual == expected

    # Size == len(li)
    li = [1, 2, 3]
    size = 3
    actual = UList.sliding_windows(li=li, size=size)
    expected = [[1, 2, 3]]
    assert actual == expected

    # Size > len(li)
    li = [1, 2, 3]
    size = 4
    actual = UList.sliding_windows(li=li, size=size)
    expected = []
    assert actual == expected

    # Empty list
    li = []
    size = 2
    actual = UList.sliding_windows(li=li, size=size)
    expected = []
    assert actual == expected

    # Longer list, size 3
    li = [1, 2, 3, 4, 5]
    size = 3
    actual = UList.sliding_windows(li=li, size=size)
    expected = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    assert actual == expected
