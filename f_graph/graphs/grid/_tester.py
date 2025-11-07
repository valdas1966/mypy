from f_graph.graphs.grid.main import GraphGrid


def test_x() -> None:
    """
    ========================================================================
     Test the x() method.
    ========================================================================
    """
    graph = GraphGrid.Factory.x()
    assert graph is not None
    assert len(graph) == 5
    cell_00 = graph.grid[0][0]
    assert graph[cell_00].key == cell_00
