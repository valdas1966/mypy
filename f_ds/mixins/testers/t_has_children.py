from f_ds.mixins import has_children
from f_ds.mixins.generators.g_has_children import GenHasChildren


def test_two_childs():
    """
    ========================================================================
     Test the two childs example.
    ========================================================================
    """
    obj = GenHasChildren.two_childs()
    assert obj.children() == {'left': 1, 'right': 2}
    obj.remove_child(key='left')
    assert obj.children() == {'right': 2}
    obj.add_child(key='left', child=1)
    assert obj.children() == {'left': 1, 'right': 2}
    obj.clear_children()
    assert obj.children() == {}
