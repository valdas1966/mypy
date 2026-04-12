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

    def to_html(self, path: str, size: int = 600) -> None:
        """
        ========================================================================
         Render this Window (and its descendants) to a standalone HTML file.
        ========================================================================
        """
        from f_gui.render.html import RenderHtml
        RenderHtml.to_file(root=self, path=path, size=size)
