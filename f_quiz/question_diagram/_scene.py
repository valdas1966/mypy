"""Bridge: build an f_gui scene (HTML card) from a QuestionDiagram.

This is the only place that imports f_gui — it turns the quiz-side spec
(nodes / edges / masked node) into a `Window` of `Label`s (nodes) joined
by `Connector` arrows (edges), laid out as a card:

    +------------------------------------------+
    |  prompt                                   |   prompt strip
    +------------------------------------------+
    |   [Premise 1]      [Premise 2]            |
    |          \\           /                    |   diagram region
    |            v       v                       |   (nodes + Connectors)
    |             [   ?   ]                      |
    +------------------------------------------+
    |   1) Option A     |   2) Option B          |   options strip
    +------------------------------------------+

Rendered to HTML by `RenderHtml`. Colors target the dark stage that
`RenderHtml.page` emits (light text), so node fills are dark.
"""
from f_gui.elements.i_2_window.main import Window
from f_gui.elements.i_1_container.main import Container
from f_gui.elements.i_1_label.main import Label
from f_gui.elements.i_1_connector.main import Connector, Routing
from f_gui.style.stroke import Stroke
from f_gui.style.border import Border
from f_gui.render.html.main import RenderHtml
from f_color.rgb import RGB
from f_ds.geometry.bounds import Bounds

from f_quiz.question_diagram.main import QuestionDiagram, DiagramNode, Reveal

# Palette (dark stage -> dark fills so the light default text reads).
_PAGE = RGB.From.hex(hex_str='#0d1117')
_PANEL = RGB.From.hex(hex_str='#161b22')
_NODE_BG = RGB.From.hex(hex_str='#30363d')
_NODE_EDGE = RGB.From.hex(hex_str='#8b949e')
_MASK_EDGE = RGB(name='orange')
_GOOD_BG = RGB.From.hex(hex_str='#238636')
_GOOD_EDGE = RGB.From.hex(hex_str='#3fb950')
_OPT_BG = RGB.From.hex(hex_str='#21262d')
_ARROW = RGB.From.hex(hex_str='#c9d1d9')

# Card layout (0-100, relative to the Window).
_PROMPT = Bounds(top=4, left=6, bottom=15, right=94)
_REGION = Bounds(top=20, left=8, bottom=74, right=92)
_OPT_L = Bounds(top=80, left=8, bottom=93, right=48)
_OPT_R = Bounds(top=80, left=52, bottom=93, right=92)


def _edge(color: RGB, width: float) -> Border:
    """
    ========================================================================
     A uniform Border of the given color / width.
    ========================================================================
    """
    return Border.Factory.all(stroke=Stroke(color=color, width=width))


def _node_label(node: DiagramNode, q: QuestionDiagram, reveal: Reveal) -> Label:
    """
    ========================================================================
     Build the Label for one node, honoring the masked / revealed state.
    ========================================================================
    """
    masked = node.key == q.masked_key
    if masked and reveal is Reveal.MASKED:
        text, bg, color, width = '?', _NODE_BG, _MASK_EDGE, 3
    elif masked:                                   # REVEALED
        text, bg, color, width = q.answer, _GOOD_BG, _GOOD_EDGE, 3
    else:
        text, bg, color, width = node.label, _NODE_BG, _NODE_EDGE, 1
    return Label(bounds=node.bounds, text=text,
                 background=bg, border=_edge(color=color, width=width))


def _diagram(q: QuestionDiagram, reveal: Reveal) -> Container:
    """
    ========================================================================
     The diagram region: a node Label per node + a Connector per edge.
    ========================================================================
     Nodes and connectors are siblings in this Container (shared frame), so
     each Connector resolves its endpoints from the node bounds.
    ========================================================================
    """
    region = Container(bounds=_REGION, background=_PANEL,
                       border=_edge(color=_NODE_EDGE, width=1))
    labels: dict[str, Label] = {}
    for node in q.nodes:
        label = _node_label(node=node, q=q, reveal=reveal)
        region.add_child(child=label)
        labels[node.key] = label
    for src, dst in q.edges:
        region.add_child(child=Connector(
            src=labels[src], dst=labels[dst],
            routing=Routing.ORTHOGONAL, arrow=True,
            stroke=Stroke(color=_ARROW, width=2)))
    return region


def _option_label(text: str, bounds: Bounds, correct: bool) -> Label:
    """
    ========================================================================
     Build one option box; the correct one is highlighted when revealed.
    ========================================================================
    """
    bg = _GOOD_BG if correct else _OPT_BG
    color = _GOOD_EDGE if correct else _NODE_EDGE
    return Label(bounds=bounds, text=text, background=bg,
                 border=_edge(color=color, width=2))


def card(q: QuestionDiagram,
         reveal: Reveal = Reveal.MASKED,
         options: list[str] | None = None) -> Window:
    """
    ========================================================================
     Assemble the full question card: prompt + diagram + two options.
    ========================================================================
     The Window's children are, in order: [prompt, diagram, option-1,
     option-2] — relied on by the tester to locate the diagram region.
    ========================================================================
    """
    opts = options if options is not None else q.options
    win = Window(background=_PAGE)
    win.add_child(child=Label(bounds=_PROMPT, text=q.text,
                              background=_PANEL,
                              border=_edge(color=_NODE_EDGE, width=1)))
    win.add_child(child=_diagram(q=q, reveal=reveal))
    for i, (opt, bounds) in enumerate(zip(opts, (_OPT_L, _OPT_R)), start=1):
        correct = reveal is Reveal.REVEALED and opt == q.answer
        prefix = '✓ ' if correct else f'{i}) '
        win.add_child(child=_option_label(text=f'{prefix}{opt}',
                                           bounds=bounds, correct=correct))
    return win


def to_html(q: QuestionDiagram,
            path: str,
            reveal: Reveal = Reveal.MASKED,
            options: list[str] | None = None) -> None:
    """
    ========================================================================
     Render the question card to a self-contained HTML file.
    ========================================================================
    """
    RenderHtml.to_file(root=card(q=q, reveal=reveal, options=options),
                       path=path)
