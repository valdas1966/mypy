from .main import GraphDict


def test_abc() -> None:
    """
    ========================================================================
     Test the abc() method.
    ========================================================================
    """
    graph = GraphDict.Factory.abc()
    assert graph is not None
    assert len(graph.nodes()) == 3
    assert graph.nodes()[0].key == 'A'
    assert graph.nodes()[1].key == 'B'
    assert graph.nodes()[2].key == 'C'
    assert graph['a'].key == 'A'
    assert graph['b'].key == 'B'
    assert graph['c'].key == 'C'
    