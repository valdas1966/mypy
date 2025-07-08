from f_core.mixins.has.row_col.main import HasRowCol


def test_has_row_col():
    """
    ============================================================================
     Test HasRowCol mixin functionality.
    ============================================================================
    """
    # Test with explicit row and col
    row_col_obj = HasRowCol(5, 10)
    assert row_col_obj.row == 5
    assert row_col_obj.col == 10
    assert row_col_obj.key_comparison() == [5, 10]
    assert row_col_obj.to_tuple() == (5, 10)
    assert str(row_col_obj) == "(5,10)"
    assert hash(row_col_obj) == hash((5, 10))
    
    # Test with None values (should default to 0)
    default_obj = HasRowCol()
    assert default_obj.row == 0
    assert default_obj.col == 0
    assert default_obj.to_tuple() == (0, 0)
    
    # Test with row only (col should take row value)
    row_only_obj = HasRowCol(3)
    assert row_only_obj.row == 3
    assert row_only_obj.col == 3
    assert row_only_obj.to_tuple() == (3, 3)
    
    # Test neighbors functionality
    neighbors = row_col_obj.neighbors()
    assert len(neighbors) == 4
    neighbor_tuples = [n.to_tuple() for n in neighbors]
    expected = [(4, 10), (5, 11), (6, 10), (5, 9)]  # N, E, S, W
    assert neighbor_tuples == expected
    
    # Test neighbors with edge case (0,0)
    edge_obj = HasRowCol(0, 0)
    edge_neighbors = edge_obj.neighbors()
    assert len(edge_neighbors) == 2  # Only E and S should be valid (>= 0)
    
    print("HasRowCol tests passed!")


if __name__ == "__main__":
    test_has_row_col()