from __future__ import annotations

from typing import TYPE_CHECKING

from f_gui.elements.i_1_container.main import Container

if TYPE_CHECKING:
    from f_color.rgb import RGB


class Window(Container):
    """
    ========================================================================
     Root Container Element (implicit full Bounds 0-100).
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 name: str = 'Window',
                 background: RGB | None = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Container.__init__(self, name=name, background=background)

    def to_html(self, path: str, size: int | None = None) -> None:
        """
        ========================================================================
         Render this Window (and its descendants) to a standalone HTML file.
        ========================================================================
         Defaults to full-screen (stage fills the viewport). Pass an int
         size for a fixed size x size centered square stage instead.
        ========================================================================
        """
        from f_gui.render.html import RenderHtml
        RenderHtml.to_file(root=self, path=path, size=size)
