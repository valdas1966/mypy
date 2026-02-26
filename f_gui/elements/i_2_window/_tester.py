import pytest
from f_gui.elements.i_2_window.main import Window
from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_1_label.main import Label
from f_ds.geometry.bounds import Bounds


@pytest.fixture
def win() -> Window:
    """
    ========================================================================
     Create a default Window.
    ========================================================================
    """
    return Window.Factory.default()


def test_bounds(win: Window) -> None:
    """
    ========================================================================
     Test that Window has full bounds (0, 0, 100, 100).
    ========================================================================
    """
    assert win.bounds.to_tuple() == (0, 0, 100, 100)


def test_name(win: Window) -> None:
    """
    ========================================================================
     Test the default name.
    ========================================================================
    """
    assert win.name == 'Window'


def test_is_container(win: Window) -> None:
    """
    ========================================================================
     Test that Window is a Container.
    ========================================================================
    """
    assert isinstance(win, Container)


def test_add_container(win: Window) -> None:
    """
    ========================================================================
     Test adding a Container to a Window.
    ========================================================================
    """
    bounds = Bounds(top=30, left=50, bottom=50, right=70)
    container = Container(bounds=bounds)
    win.add(child=container)
    assert len(win.children) == 1
    assert container.parent is win


def test_nested_layout(win: Window) -> None:
    """
    ========================================================================
     Test the full nested layout: Window > Container > Label.
    ========================================================================
    """
    # Add Container to Window
    bounds_c = Bounds(top=30, left=50, bottom=50, right=70)
    container = Container(bounds=bounds_c)
    win.add(child=container)
    # Add Label to Container
    bounds_l = Bounds(top=20, left=10, bottom=40, right=30)
    label = Label(bounds=bounds_l, text='Hello')
    container.add(child=label)
    # Verify hierarchy
    assert label.parent is container
    assert container.parent is win
    assert win.parent is None
    # Verify children
    assert len(win.children) == 1
    assert len(container.children) == 1
    assert label.text == 'Hello'


def test_str(win: Window) -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(win) == 'Window(0, 0, 100, 100)'
