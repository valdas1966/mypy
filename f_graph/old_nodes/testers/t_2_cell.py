from f_graph.nodes.generators.g_2_cell import GenNodeCell


def test_by_row_col():
    """
    ========================================================================
     Test the by_row_col() method.
    ========================================================================
    """
    node = GenNodeCell.by_row_col(row=1, col=2)
    assert node.cell.row == 1   
    assert node.cell.col == 2


def test_str():
    """
    ========================================================================
     Test the str() method.
    ========================================================================
    """
    node = GenNodeCell.by_row_col(row=1, col=2)
    assert str(node) == '(1,2)'
