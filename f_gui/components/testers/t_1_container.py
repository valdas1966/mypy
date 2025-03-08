from f_gui.components.generators.g_1_container import GenContainer


def test_two_childs():
    """
    ========================================================================
     Test the two childs.
    ========================================================================
    """
    container = GenContainer.two_childs()
    assert container.position == (0, 0, 100, 100)
    assert container.children().keys() == {'left', 'right'}
    assert container.children()['left'].position == (10, 10, 35, 80)
    assert container.children()['right'].position == (10, 55, 35, 80)
