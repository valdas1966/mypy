from __future__ import annotations

from enum import Enum

from f_gui.elements.i_0_element.main import Element
from f_gui.style.stroke import Stroke
from f_ds.geometry.bounds import Bounds
from f_ds.geometry.pointxy import PointXY
from f_ds.geometry.side import Side


class Routing(Enum):
    """
    ========================================================================
     Routing — how a Connector shapes its path between its two anchors.
    ========================================================================
     DIRECT     a single straight segment (anchor -> anchor).
     ORTHOGONAL a 90-degree elbow: leaves and enters each anchor along its
                side's outward normal, joined by a horizontal/vertical
                mid-line (1-2 bends). Obstacle avoidance is out of scope.
    ========================================================================
    """
    DIRECT = 'direct'
    ORTHOGONAL = 'orthogonal'


class Connector(Element):
    """
    ============================================================================
     Connector — an auto-routing line/arrow attached to two Elements.
    ============================================================================
     Holds references to a source and a destination `Element`, plus the `Side`
     of each to attach to (`None` = auto-pick the nearest facing sides). On
     every render it pulls the two connection points live from the elements'
     `bounds` (so the connector follows when they move) and produces a `path`:
     a single straight segment (DIRECT) or a 90-degree elbow polyline
     (ORTHOGONAL). Appearance is a `Stroke` (the value object shared with
     `Line` and `Border`); an optional arrowhead sits at the destination end.

     The source, destination and Connector must share a parent (the same
     0-100 coordinate frame) — the renderer draws the Connector as an SVG
     overlay filling that parent.
    ============================================================================
    """

    # Factory
    Factory: type = None

    # Length (0-100 units) each orthogonal leg leaves its anchor by before
    # turning — keeps the exit/entry perpendicular to the attached side.
    _STUB = 6

    def __init__(self,
                 src: Element,
                 dst: Element,
                 src_side: Side | None = None,
                 dst_side: Side | None = None,
                 stroke: Stroke | None = None,
                 arrow: bool = True,
                 routing: Routing = Routing.DIRECT,
                 name: str = 'Connector') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
         src_side / dst_side default to None (auto-pick nearest facing sides);
         arrow defaults to True (a connector usually points at its target).
        ========================================================================
        """
        Element.__init__(self, name=name)
        self._src = src
        self._dst = dst
        self._src_side = src_side
        self._dst_side = dst_side
        self._stroke = stroke or Stroke()
        self._arrow = arrow
        self._routing = routing

    @property
    def src(self) -> Element:
        """
        ========================================================================
         Get the source Element (the path starts at its anchor).
        ========================================================================
        """
        return self._src

    @property
    def dst(self) -> Element:
        """
        ========================================================================
         Get the destination Element (the arrowhead sits at its anchor).
        ========================================================================
        """
        return self._dst

    @property
    def src_side(self) -> Side | None:
        """
        ========================================================================
         Get the source attach Side (None = auto-pick the nearest side).
        ========================================================================
        """
        return self._src_side

    @property
    def dst_side(self) -> Side | None:
        """
        ========================================================================
         Get the destination attach Side (None = auto-pick the nearest side).
        ========================================================================
        """
        return self._dst_side

    @property
    def stroke(self) -> Stroke:
        """
        ========================================================================
         Get the Stroke (color / width / style) of the Connector.
        ========================================================================
        """
        return self._stroke

    @property
    def arrow(self) -> bool:
        """
        ========================================================================
         Whether an arrowhead is drawn at the destination end.
        ========================================================================
        """
        return self._arrow

    @property
    def routing(self) -> Routing:
        """
        ========================================================================
         Get the Routing (DIRECT straight / ORTHOGONAL 90-degree elbow).
        ========================================================================
        """
        return self._routing

    @property
    def path(self) -> list[PointXY]:
        """
        ========================================================================
         The polyline vertices (>= 2), computed live from the elements' bounds.
        ========================================================================
         DIRECT -> [anchor_src, anchor_dst]; ORTHOGONAL -> an axis-aligned
         elbow. Recomputed on each access, so it tracks element movement.
        ========================================================================
        """
        side_src, side_dst = self._sides()
        p_src = self._src.bounds.anchor(side=side_src)
        p_dst = self._dst.bounds.anchor(side=side_dst)
        if self._routing is Routing.ORTHOGONAL:
            return Connector._orthogonal(p_src=p_src, side_src=side_src,
                                         p_dst=p_dst, side_dst=side_dst)
        return [p_src, p_dst]

    @property
    def bounds(self) -> Bounds[float]:
        """
        ========================================================================
         Bounding box of the current path (kept live as the elements move).
        ========================================================================
        """
        pts = self.path
        xs = [p.x for p in pts]
        ys = [p.y for p in pts]
        return Bounds(top=min(ys), left=min(xs),
                      bottom=max(ys), right=max(xs))

    def _sides(self) -> tuple[Side, Side]:
        """
        ========================================================================
         Resolve the attach sides, auto-picking either one left as None.
        ========================================================================
        """
        side_src, side_dst = self._src_side, self._dst_side
        if side_src is None or side_dst is None:
            auto_src, auto_dst = self._auto_sides()
            side_src = side_src or auto_src
            side_dst = side_dst or auto_dst
        return side_src, side_dst

    def _auto_sides(self) -> tuple[Side, Side]:
        """
        ========================================================================
         Nearest facing sides from the two elements' relative centers.
        ========================================================================
         Horizontal gap dominates -> RIGHT/LEFT pair; vertical -> BOTTOM/TOP.
        ========================================================================
        """
        a, b = self._src.bounds, self._dst.bounds
        dx = (b.left + b.right) / 2 - (a.left + a.right) / 2
        dy = (b.top + b.bottom) / 2 - (a.top + a.bottom) / 2
        if abs(dx) >= abs(dy):
            return (Side.RIGHT, Side.LEFT) if dx >= 0 \
                else (Side.LEFT, Side.RIGHT)
        return (Side.BOTTOM, Side.TOP) if dy >= 0 \
            else (Side.TOP, Side.BOTTOM)

    @staticmethod
    def _orthogonal(p_src: PointXY,
                    side_src: Side,
                    p_dst: PointXY,
                    side_dst: Side) -> list[PointXY]:
        """
        ========================================================================
         Build an axis-aligned (90-degree) elbow path between two anchors.
        ========================================================================
         Each anchor first steps out by `_STUB` along its side's normal, then
         the two stubs are joined: a vertical mid-line for two horizontal
         normals, a horizontal mid-line for two vertical normals, or a single
         corner for a mixed pair. Collinear points are then dropped.
        ========================================================================
        """
        nx_s, ny_s = side_src.normal
        nx_d, ny_d = side_dst.normal
        stub = Connector._STUB
        a1 = PointXY(x=p_src.x + nx_s * stub, y=p_src.y + ny_s * stub)
        b1 = PointXY(x=p_dst.x + nx_d * stub, y=p_dst.y + ny_d * stub)
        src_h = nx_s != 0          # source normal is horizontal (LEFT/RIGHT)
        dst_h = nx_d != 0          # destination normal is horizontal
        if src_h and dst_h:
            midx = (a1.x + b1.x) / 2
            mids = [PointXY(x=midx, y=a1.y), PointXY(x=midx, y=b1.y)]
        elif not src_h and not dst_h:
            midy = (a1.y + b1.y) / 2
            mids = [PointXY(x=a1.x, y=midy), PointXY(x=b1.x, y=midy)]
        elif src_h:                # horizontal out, vertical in
            mids = [PointXY(x=b1.x, y=a1.y)]
        else:                      # vertical out, horizontal in
            mids = [PointXY(x=a1.x, y=b1.y)]
        return Connector._simplify(pts=[p_src, a1, *mids, b1, p_dst])

    @staticmethod
    def _simplify(pts: list[PointXY]) -> list[PointXY]:
        """
        ========================================================================
         Drop consecutive duplicate and collinear vertices from a path.
        ========================================================================
        """
        out: list[PointXY] = [pts[0]]
        for p in pts[1:]:
            if p != out[-1]:
                out.append(p)
        i = 1
        while i < len(out) - 1:
            a, b, c = out[i - 1], out[i], out[i + 1]
            if (a.x == b.x == c.x) or (a.y == b.y == c.y):
                del out[i]
            else:
                i += 1
        return out

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the Connector.
        ========================================================================
        """
        return f'{self.name}({self._src.name}->{self._dst.name})'
