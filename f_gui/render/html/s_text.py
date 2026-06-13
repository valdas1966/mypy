"""Study: TextStyle — the visual appearance of a Label's text.

One horizontal band per TextStyle dimension, each cell a white chip whose
Label text is rendered with the labelled style (light fill so colored /
dark text stays readable):

  Presets      : style=None (baseline) vs default / code / body / title
  Font         : monospace / sans-serif / serif / cursive / fantasy
  Size         : 10 / 14 / 18 / 24 / 32 px
  Weight       : normal vs bold
  Color        : a crimson -> steelblue gradient (text colored, label = hex)
  Combinations : preset + color + size mixes

Run:  python -m f_gui.render.html.s_text   (then open text.html)
"""
from f_gui.elements import Window, Container, Label
from f_gui.style import Stroke, Border, TextStyle
from f_gui.render import RenderHtml
from f_ds.geometry import Bounds
from f_color import RGB


# Header look (dark, on the gainsboro stage) + thin chip border.
HEADER = TextStyle(font='sans-serif', size=13, bold=True, color=RGB('black'))
BORDER = Border.Factory.all(stroke=Stroke(color=RGB('silver'), width=1))

win = Window(background=RGB('gainsboro'))


def section(header: str, top0: float, bot0: float,
            items: list[tuple[str, TextStyle | None]],
            header_h: float = 4.0, pad: float = 1.0) -> None:
    """Place a full-width header + a row of white chips (one per item)."""
    win.add_child(Label(bounds=Bounds(top0, 1, top0 + header_h, 99),
                        text=header, style=HEADER))
    ctop, w = top0 + header_h, 100 / len(items)
    for i, (text, style) in enumerate(items):
        chip = Container(bounds=Bounds(top=ctop + pad, left=i * w + pad,
                                       bottom=bot0 - pad, right=(i + 1) * w - pad),
                         background=RGB('white'), border=BORDER)
        chip.add_child(Label(text=text, style=style))
        win.add_child(chip)


# ── Presets: None (baseline) vs the four Factory presets ──────────────
section('Presets — style=None (baseline) vs Factory presets', 0, 16, [
    ('None (baseline)', None),
    ('default()', TextStyle.Factory.default()),
    ('code()', TextStyle.Factory.code()),
    ('body()', TextStyle.Factory.body()),
    ('title()', TextStyle.Factory.title()),
])

# ── Font family (size fixed at 16px) ──────────────────────────────────
section('Font family (size=16)', 16, 33, [
    (font, TextStyle(font=font, size=16))
    for font in ('monospace', 'sans-serif', 'serif', 'cursive', 'fantasy')
])

# ── Size (font fixed at sans-serif) ───────────────────────────────────
section('Size — px (font=sans-serif)', 33, 50, [
    (f'{size}px', TextStyle(font='sans-serif', size=size))
    for size in (10, 14, 18, 24, 32)
])

# ── Weight (size 20, sans-serif) ──────────────────────────────────────
section('Weight (size=20, font=sans-serif)', 50, 64, [
    ('normal', TextStyle(font='sans-serif', size=20, bold=False)),
    ('bold', TextStyle(font='sans-serif', size=20, bold=True)),
])

# ── Color: crimson -> steelblue gradient (label = each color's hex) ───
grad = RGB.Factory.gradient(a=RGB('crimson'), b=RGB('steelblue'), n=6)
section('Color — gradient (size=18, bold)', 64, 82, [
    (col.to.hex(), TextStyle(font='sans-serif', size=18, bold=True, color=col))
    for col in grad
])

# ── Several fields set together in one style (vs the isolated bands) ──
section('Several fields in one style (font + size + weight + color)',
        82, 100, [
    ('title + red', TextStyle(size=18, bold=True, color=RGB('crimson'))),
    ('body bold blue',
     TextStyle(font='sans-serif', size=14, bold=True, color=RGB('steelblue'))),
    ('code + green', TextStyle(font='monospace', size=13, color=RGB('green'))),
    ('serif 24 purple', TextStyle(font='serif', size=24, color=RGB('purple'))),
])

RenderHtml.to_file(root=win, path='text.html')
