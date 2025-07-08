from f_core.mixins.has.rows_cols.main import HasRowsCols


def test_has_rows_cols():
    """
    ============================================================================
     Test HasRowsCols mixin functionality.
    ============================================================================
    """
    # Test with explicit rows and cols
    rows_cols_obj = HasRowsCols(5, 10)
    assert rows_cols_obj.rows == 5
    assert rows_cols_obj.cols == 10
    assert rows_cols_obj.shape() == "(5,10)"
    assert len(rows_cols_obj) == 50
    assert rows_cols_obj.key_comparison() == [50, 5]
    assert str(rows_cols_obj) == "(5,10)"
    assert hash(rows_cols_obj) == hash((5, 10))
    
    # Test with rows only (cols should take rows value)
    square_obj = HasRowsCols(3)
    assert square_obj.rows == 3
    assert square_obj.cols == 3
    assert square_obj.shape() == "(3,3)"
    assert len(square_obj) == 9
    assert str(square_obj) == "(3,3)"
    
    # Test is_within functionality
    assert rows_cols_obj.is_within(0, 0) == True
    assert rows_cols_obj.is_within(4, 9) == True
    assert rows_cols_obj.is_within(5, 10) == False  # Out of bounds
    assert rows_cols_obj.is_within(-1, 0) == False  # Negative row
    assert rows_cols_obj.is_within(0, -1) == False  # Negative col
    assert rows_cols_obj.is_within(2, 5) == True   # Within bounds
    
    # Test edge cases
    single_obj = HasRowsCols(1, 1)
    assert single_obj.is_within(0, 0) == True
    assert single_obj.is_within(0, 1) == False
    assert single_obj.is_within(1, 0) == False
    
    print("HasRowsCols tests passed!")


if __name__ == "__main__":
    test_has_rows_cols()