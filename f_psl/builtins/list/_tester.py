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
    assert UList.sliding_windows(li=li, size=2) == [[1, 2], [2, 3]]

    # Size 1
    li = [1, 2, 3]
    assert UList.sliding_windows(li=li, size=1) == [[1], [2], [3]]

    # Size == len(li)
    li = [1, 2, 3]
    assert UList.sliding_windows(li=li, size=3) == [[1, 2, 3]]

    # Size > len(li)
    li = [1, 2, 3]
    assert UList.sliding_windows(li=li, size=4) == []

    # Empty list
    li = []
    assert UList.sliding_windows(li=li, size=2) == []

    # Longer list, size 3
    li = [1, 2, 3, 4, 5]
    assert UList.sliding_windows(li=li, size=3) \
        == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
