from f_ds.graphs.quick.main import GraphQuick


def test_x() -> None:
    """
    ========================================================================
     Test the x() method.
    ========================================================================
    """
    graph = GraphQuick.Factory.x()
    assert graph is not None
    assert len(graph) == 5
    cell_00 = graph.grid[0][0]
    assert graph[cell_00].key == cell_00
