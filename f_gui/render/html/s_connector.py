"""Study: Connector — an auto-routing line/arrow between two Elements.

Each cell holds a source box (top-left) and a destination box (bottom-
right) plus a Connector between them. Shows DIRECT vs ORTHOGONAL routing,
auto-picked vs explicit sides, the four auto directions, and stroke
variants. The connector pulls its endpoints live from the two boxes'
bounds, so moving a box moves the line.

Run:  python -m f_gui.render.html.s_connector   (then open connector.html)
"""
from f_gui.elements import Window, Container, Label, Connector, Routing
from f_gui.style import Stroke, LineStyle, Border
from f_gui.render import RenderHtml
from f_ds.geometry import Bounds, Side
from f_color import RGB


def cell_bounds(r: int, c: int, pad: float = 2.0) -> Bounds:
    h, w = 100 / 2, 100 / 4
    return Bounds(top=r * h + pad, left=c * w + pad,
                  bottom=(r + 1) * h - pad, right=(c + 1) * w - pad)


def box(bounds: Bounds, color: str) -> Container:
    return Container(bounds=bounds, background=RGB(color),
                     border=Border.Factory.all(
                         stroke=Stroke(color=RGB('black'), width=1)))


def cell(i: int, text: str, src: Container, dst: Container,
         conn: Connector) -> Container:
    r, c = divmod(i, 4)
    edge = Border.Factory.all(stroke=Stroke(color=RGB('black'), width=1))
    con = Container(bounds=cell_bounds(r, c), background=RGB('white'),
                    border=edge)
    # src, dst and the connector are siblings (shared coordinate frame).
    con.add_child(src)
    con.add_child(dst)
    con.add_child(conn)
    con.add_child(Label(bounds=Bounds(82, 2, 98, 98), text=text))
    return con


def stroke(color: str, width: float = 2,
           style: LineStyle = LineStyle.SOLID) -> Stroke:
    return Stroke(color=RGB(color), width=width, style=style)


# Reusable layouts (relative to a cell).
TL = Bounds(top=12, left=8, bottom=34, right=34)     # top-left box
BR = Bounds(top=54, left=62, bottom=76, right=90)    # bottom-right box
ML = Bounds(top=34, left=6, bottom=56, right=30)     # mid-left box
MR = Bounds(top=34, left=66, bottom=56, right=92)    # mid-right box
TM = Bounds(top=8, left=38, bottom=30, right=64)     # top-mid box
BM = Bounds(top=60, left=38, bottom=82, right=64)    # bottom-mid box

win = Window(background=RGB('gainsboro'))

cells = []

# 1. DIRECT (auto sides, arrow).
a, b = box(TL, 'lightyellow'), box(BR, 'lightyellow')
cells.append(('direct', a, b, Connector(src=a, dst=b, stroke=stroke('crimson'))))

# 2. ORTHOGONAL (auto sides, arrow).
a, b = box(TL, 'lightyellow'), box(BR, 'lightyellow')
cells.append(('orthogonal', a, b,
              Connector(src=a, dst=b, routing=Routing.ORTHOGONAL,
                        stroke=stroke('navy'))))

# 3. DIRECT dashed.
a, b = box(TL, 'lightyellow'), box(BR, 'lightyellow')
cells.append(('dashed', a, b,
              Connector(src=a, dst=b,
                        stroke=stroke('green', style=LineStyle.DASHED))))

# 4. ORTHOGONAL thick.
a, b = box(TL, 'lightyellow'), box(BR, 'lightyellow')
cells.append(('thick (5px)', a, b,
              Connector(src=a, dst=b, routing=Routing.ORTHOGONAL,
                        stroke=stroke('purple', width=5))))

# 5. auto: left -> right (horizontal gap).
a, b = box(ML, 'lightcyan'), box(MR, 'lightcyan')
cells.append(('auto: L->R', a, b, Connector(src=a, dst=b, stroke=stroke('teal'))))

# 6. auto: top -> bottom (vertical gap), orthogonal.
a, b = box(TM, 'lightcyan'), box(BM, 'lightcyan')
cells.append(('auto: T->B', a, b,
              Connector(src=a, dst=b, routing=Routing.ORTHOGONAL,
                        stroke=stroke('darkorange'))))

# 7. explicit sides TOP -> TOP, orthogonal.
a, b = box(ML, 'mistyrose'), box(MR, 'mistyrose')
cells.append(('explicit T->T', a, b,
              Connector(src=a, dst=b, src_side=Side.TOP, dst_side=Side.TOP,
                        routing=Routing.ORTHOGONAL, stroke=stroke('maroon'))))

# 8. DIRECT, no arrow.
a, b = box(TL, 'lightyellow'), box(BR, 'lightyellow')
cells.append(('no arrow', a, b,
              Connector(src=a, dst=b, arrow=False, stroke=stroke('black'))))

for i, (text, src, dst, conn) in enumerate(cells):
    win.add_child(cell(i, text, src, dst, conn))

RenderHtml.to_file(root=win, path='connector.html')
