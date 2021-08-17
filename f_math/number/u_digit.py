
def sum(a, b, prev=0):
    """
    ============================================================================
     Description: Return Tuple(Remainder, Whole) of Result of adding two digits.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int (Digit to Add).
        2. b : int (Digit to Add).
        3. prev : int (Whole from the previous digits' adding).
    ============================================================================
     Return: tuple(int, int) (Remainder, Whole)
    ============================================================================
    """
    assert type(a) == int
    assert type(b) == int
    assert type(prev) == int
    assert 0 <= a <= 9
    assert 0 <= b <= 9
    assert 0 <= prev <= 1
    c = a + b + prev
    remainder = c % 10
    whole = c // 10
    return remainder, whole


def mult(a, b, prev=0):
    """
    ============================================================================
     Description: Return Tuple(Remainder, Whole) representing the result of
                    multiplying two digits.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. a : int (Digit to Multiply).
        2. b : int (Digit to Multiply).
        3. prev : int (Whole from the previous digits' multiplying).
    ============================================================================
     Return: tuple(int, int) (Remainder, Whole)
    ============================================================================
    """
    assert type(a) == int
    assert type(b) == int
    assert type(prev) == int
    assert 0 <= a <= 9
    assert 0 <= b <= 9
    assert 0 <= prev <= 8
    c = (a * b) + prev
    remainder = c % 10
    whole = c // 10
    return remainder, whole
