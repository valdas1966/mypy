from f_graph.path.generators.g_graph_map import GenGraphMap


def test_graph_map() -> None:
    """
    ============================================================================
     Test the GraphMap class.
    ============================================================================
    """
    graph = GenGraphMap.test()
    assert graph.domain == 'temp'
    assert graph.name == 'map_grid'
    assert len(graph.nodes()) == 8
