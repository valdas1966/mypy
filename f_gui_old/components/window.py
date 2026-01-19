from f_gui_old.components.component import Component


class Window(Component):
    """
    ========================================================================
     A UI component that can contain children and manage layout.
    ========================================================================
    """

    def __init__(self,
                 key: str = 'Window'  # Unique id for the Window
                 ) -> None:
        """
        ========================================================================
         Initialize the Window.
        ========================================================================
        """
        Component.__init__(self, name=key)

