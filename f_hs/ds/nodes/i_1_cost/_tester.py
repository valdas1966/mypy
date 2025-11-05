from f_hs.ds.nodes.i_1_cost import NodeCost


def test_g() -> None:
    """
    ========================================================================
     Test the g-value of the node.
    ========================================================================
    """
    node_00 = NodeCost.Factory.cell_00()
    assert node_00.g == 0  
    node_01 = NodeCost.Factory.cell_01()
    node_01.parent = node_00
    assert node_01.g == 1    
    
    
def test_key_comparison() -> None:
    """
    ========================================================================
     Test the key comparison of the node.
    ========================================================================
    """
    node_00 = NodeCost.Factory.cell_00()
    # (g=0, h=5, f=5) == (g=0, h=5, f=5)
    assert node_00 == node_00
    node_01 = NodeCost.Factory.cell_01()
    # (g=0, h=4, f=4) < (g=0, h=5, f=5)
    assert node_01 < node_00
    node_01.parent = node_00
    # (g=1, h=4, f=5) < (g=0, h=5, f=5)
    assert node_01 < node_00
    node_11 = NodeCost.Factory.cell_11()
    # (g=0, h=3, f=3) < (g=0, h=5, f=5)
    assert node_11 < node_00
    # (g=0, h=3, f=3) < (g=1, h=4, f=5)
    assert node_11 < node_01


def test_f() -> None:
    """
    ========================================================================
     Test the f-value of the node.
    ========================================================================
    """
    node_00 = NodeCost.Factory.cell_00()
    node_01 = NodeCost.Factory.cell_01()
    assert node_01.f() == 4
    node_01.parent = node_00
    assert node_01.f() == 5
    node_11 = NodeCost.Factory.cell_11()
    if node_11 < node_01.parent:
        node_01.parent = node_11
    assert node_01.f() == 5
    assert node_01.parent == node_11
