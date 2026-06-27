from __future__ import annotations

from f_gui.elements.i_0_element.main import Element
from f_gui.style.stroke import Stroke
from f_ds.geometry.bounds import Bounds
from f_ds.geometry.pointxy import PointXY


class Line(Element):
    """
    ========================================================================
     Line Element (a directed segment between two Points).
    ========================================================================
     Defined by two endpoints p1 -> p2 in the normalized 0-100 space
     (relative to the parent). Appearance is a `Stroke` (color, width,
     style) shared with Border edges; geometry and an optional arrowhead at
     p2 are Line's own. The Element bounds are the bounding box of the
     two endpoints.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 p1: PointXY,
                 p2: PointXY,
                 stroke: Stroke | None = None,
                 arrow: bool = False,
                 name: str = 'Line') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Element.__init__(self, bounds=Line._bbox(p1=p1, p2=p2), name=name)
        self._p1 = p1
        self._p2 = p2
        self._stroke = stroke or Stroke()
        self._arrow = arrow

    @property
    def p1(self) -> PointXY:
        """
        ========================================================================
         Get the start PointXY of the Line.
        ========================================================================
        """
        return self._p1

    @property
    def p2(self) -> PointXY:
        """
        ========================================================================
         Get the end PointXY of the Line (where the arrowhead sits, if any).
        ========================================================================
        """
        return self._p2

    @property
    def stroke(self) -> Stroke:
        """
        ========================================================================
         Get the Stroke (color / width / style) of the Line.
        ========================================================================
        """
        return self._stroke

    @property
    def arrow(self) -> bool:
        """
        ========================================================================
         Whether an arrowhead is drawn at the end PointXY (p2).
        ========================================================================
        """
        return self._arrow

    @staticmethod
    def _bbox(p1: PointXY, p2: PointXY) -> Bounds[float]:
        """
        ========================================================================
         Bounding box (Bounds) enclosing the two endpoints.
        ========================================================================
        """
        return Bounds(top=min(p1.y, p2.y),
                      left=min(p1.x, p2.x),
                      bottom=max(p1.y, p2.y),
                      right=max(p1.x, p2.x))

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Line.
        ========================================================================
        """
        return f'{self.name}{self._p1}->{self._p2}'
