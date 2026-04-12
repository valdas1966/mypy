from f_gui.elements.i_2_window.main import Window
from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_1_label.main import Label
from f_ds.geometry.bounds import Bounds


def test_bounds() -> None:
    """
    ========================================================================
     Test that Window has full bounds (0, 0, 100, 100).
    ========================================================================
    """
    assert Window.Factory.default().bounds.to_tuple() == (0, 0, 100, 100)


def test_name() -> None:
    """
    ========================================================================
     Test the default name.
    ========================================================================
    """
    assert Window.Factory.default().name == 'Window'


def test_is_container() -> None:
    """
    ========================================================================
     Test that Window is a Container.
    ========================================================================
    """
    assert isinstance(Window.Factory.default(), Container)


def test_add_container() -> None:
    """
    ========================================================================
     Test adding a Container to a Window.
    ========================================================================
    """
    win = Window.Factory.default()
    container = Container(bounds=Bounds(top=30, left=50, bottom=50, right=70))
    win.add_child(child=container)
    assert len(win.children) == 1
    assert container.parent is win


def test_nested_layout() -> None:
    """
    ========================================================================
     Test the full nested layout: Window > Container > Label.
    ========================================================================
    """
    win = Window.Factory.default()
    container = Container(bounds=Bounds(top=30, left=50, bottom=50, right=70))
    label = Label(bounds=Bounds(top=20, left=10, bottom=40, right=30),
                  text='Hello')
    win.add_child(child=container)
    container.add_child(child=label)
    assert label.parent is container
    assert container.parent is win
    assert win.parent is None
    assert len(win.children) == 1
    assert len(container.children) == 1
    assert label.text == 'Hello'


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(Window.Factory.default()) == 'Window(0, 0, 100, 100)'
