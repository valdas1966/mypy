from f_graph.old_path.generators.g_node import GenNode


def test_name() -> None:
    """
    ============================================================================
     Test name attribute.
    ============================================================================
    """
    start, pre_goal, goal = GenNode.gen_3x3()
    assert start.cell.row == 0 and start.cell.col == 0
    assert pre_goal.cell.row == 1 and pre_goal.cell.col == 2
    assert goal.cell.row == 2 and goal.cell.col == 2


def test_g() -> None:
    """
    ============================================================================
     Test g attribute.
    ============================================================================
    """
    start, pre_goal, goal = GenNode.gen_3x3()
    assert start.g == 0
    assert pre_goal.g == 0
    assert goal.g == 1


def test_h() -> None:
    """
    ============================================================================
     Test h attribute.
    ============================================================================
    """
    start, pre_goal, goal = GenNode.gen_3x3()
    assert start.h == 4
    assert pre_goal.h == 1
    assert goal.h == 0


def test_f() -> None:
    """
    ============================================================================
     Test f attribute.
    ============================================================================
    """
    start, pre_goal, goal = GenNode.gen_3x3()
    assert start.f() == 4
    assert pre_goal.f() == 1
    assert goal.f() == 1


def test_parent() -> None:
    """
    ============================================================================
     Test parent attribute.
    ============================================================================
    """
    start, pre_goal, goal = GenNode.gen_3x3()
    assert start.parent is None
    assert pre_goal.parent is None
    assert goal.parent == pre_goal


def test_path_from_node() -> None:
    """
    ============================================================================
     Test path_from_node() Function.
    ============================================================================
    """
    start, pre_goal, goal = GenNode.gen_3x3()
    assert start.path_from_node(node=start) == [start]


def test_str() -> None:
    """
    ============================================================================
     Test __str__() Function.
    ============================================================================
    """
    start, _, goal = GenNode.gen_3x3()
    assert str(start) == '(0,0)'
    assert str(goal) == '(2,2)'
