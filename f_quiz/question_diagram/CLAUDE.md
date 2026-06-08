# QuestionDiagram

## Purpose

A quiz question whose **stimulus is an `f_gui` diagram** — boxes (nodes)
joined by arrows (edges) — with exactly one **masked node**. The student
picks the masked node's label from two options. Unlike `QuestionVisual`
(which points at a hand-authored SVG on Google Drive that nothing in
`f_quiz` actually renders), a `QuestionDiagram` **builds and renders its
own visual** from existing `f_gui` elements.

```
nodes = boxes      -> a Label each
edges = arrows     -> a Connector each (the f_gui directed connector)
masked node        -> shown as '?', its true label IS the answer
```

The masked node's label is the **correct answer** (not duplicated); only
the `wrong` distractor is supplied.

## Public API

### `Reveal` enum

```python
class Reveal(Enum):
    MASKED    # masked node shows '?'              (the question)
    REVEALED  # masked node shows the answer, green (the answer key)
```

### `DiagramNode` (dataclass)

```python
@dataclass
class DiagramNode:
    key: str        # id, referenced by edges and masked_key
    bounds: Bounds  # 0-100, relative to the diagram region
    label: str      # box text (the answer, for the masked node)
```

### `QuestionDiagram(QuestionOptions)`

```python
def __init__(self,
             topic: str,
             nodes: list[DiagramNode],
             edges: list[tuple[str, str]],   # (src_key, dst_key)
             masked_key: str,
             wrong: str) -> None             # answer = masked node's label

@property
def topic / nodes / edges / masked_key
# inherited: text, answer, wrong, options (shuffled [answer, wrong])

def to_scene(self, reveal=Reveal.MASKED, options=None) -> Window
def to_html(self, path, reveal=Reveal.MASKED, options=None) -> None
```

`options` pins the (otherwise shuffled) option order so a MASKED card and
its REVEALED answer key stay consistent.

## Inheritance

```
Question (text, answer)
  └── QuestionOptions (+ wrong, options)
        └── QuestionDiagram (+ topic, nodes, edges, masked_key; f_gui scene)
```

Being a `QuestionOptions`, it is **drop-in compatible** with the existing
`ExamRunner` / `ExamGuiOptions` (answer-checking, score, 1/2 selection).
The `f_gui` card is the *visual*; interaction stays in those runners.

## The scene bridge — `_scene.py`

`_scene.py` is the **only** module that imports `f_gui` (keeping `f_gui`
domain-free). It assembles a card `Window`:

| Region | f_gui |
|--------|-------|
| prompt strip (top) | a `Label` |
| diagram region (middle) | a `Container` holding a `Label` per node + a `Connector` per edge (nodes & connectors are siblings → connectors resolve endpoints from node bounds) |
| options strip (bottom) | two `Label` boxes (`1) …` / `2) …`; correct one turns green + `✓` when revealed) |

Node fills are **dark** because `RenderHtml.page` emits a dark stage with
light default text (text color is not yet an `f_gui` feature). Edges use
`Routing.ORTHOGONAL` arrows; the arrowhead lands on the masked node's
border (the `refX=10` connector fix).

`QuestionDiagram.to_scene` / `to_html` lazy-import `_scene` (mirrors
`Window.to_html`), so the data model only pulls in `f_gui` when rendering.

## Factory Presets

| Method              | Diagram                                            |
|---------------------|----------------------------------------------------|
| `argument_anatomy()`| Premise 1 + Premise 2 → masked **Conclusion** (vs Premise) |
| `modus_ponens()`    | `If P then Q` + `P` → masked **Q** (vs P)          |

## Dependencies

| Import | Purpose |
|--------|---------|
| `f_quiz.question_options.QuestionOptions` | Base class (answer + wrong + options) |
| `f_ds.geometry.bounds.Bounds` | Node position/size |
| `f_gui.*` (via `_scene.py` only) | `Window`/`Container`/`Label`/`Connector`/`Stroke`/`Border` + `RenderHtml` |
| `f_color.rgb.RGB` (via `_scene.py`) | Node / option / arrow colors |

## Study

`_study.py` writes question + answer-key cards for both presets:

```bash
python -m f_quiz.question_diagram._study
# open diagram_argument_q.html / _a.html, diagram_modus_q.html / _a.html
```

## Possible Extensions

- A `Reveal.WRONG` state (highlight the student's wrong pick in pink).
- Label **text color** in `f_gui` → light nodes / themed cards.
- Auto-layout (rows/graph) so a diagram is just nodes + edges, no bounds.
- An interactive HTML exam (click an option) via a thin JS shell, or a
  `RenderTk` backend to embed the same scene in the tkinter exams.
- Load diagram specs from the `Visual` sheet (extend the loaders).
