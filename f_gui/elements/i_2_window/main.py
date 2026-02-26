from f_gui.elements.i_1_container.main import Container


class Window(Container):
    """
    ========================================================================
     Root Container Element (implicit full Bounds 0-100).
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, name: str = 'Window') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Container.__init__(self, name=name)
