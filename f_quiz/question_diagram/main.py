from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from f_ds.geometry.bounds import Bounds
from f_quiz.question_options.main import QuestionOptions

if TYPE_CHECKING:
    from f_gui.elements.i_2_window.main import Window


class Reveal(Enum):
    """
    ========================================================================
     Reveal — which state a QuestionDiagram scene is rendered in.
    ========================================================================
     MASKED   the masked node shows '?' (the question the student sees).
     REVEALED the masked node shows the answer, highlighted green, and the
              correct option box is marked (the answer key / feedback).
    ========================================================================
    """
    MASKED = 'masked'
    REVEALED = 'revealed'


@dataclass
class DiagramNode:
    """
    ========================================================================
     DiagramNode — one box in a question's diagram.
    ========================================================================
     key    a stable id, referenced by edges and by `masked_key`.
     bounds position/size (0-100) relative to the diagram region.
     label  the text shown in the box (for the masked node this is the
            correct answer, hidden behind '?' until revealed).
    ========================================================================
    """
    key: str
    bounds: Bounds
    label: str


class QuestionDiagram(QuestionOptions):
    """
    ============================================================================
     Quiz Question whose stimulus is an f_gui diagram with one masked node.
    ============================================================================
     The diagram is a set of nodes (boxes) joined by directed edges (arrows).
     Exactly one node — `masked_key` — is hidden: the student must pick its
     correct label from two options. The masked node's label IS the correct
     answer (so it is not duplicated); only the `wrong` distractor is given.

     The diagram is built from existing f_gui elements (a `Label` per node,
     a `Connector` per edge) and rendered to an HTML card by `RenderHtml` —
     see `_scene.py`. This keeps `f_gui` domain-free: the quiz-specific
     scene assembly lives here.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 topic: str,
                 nodes: list[DiagramNode],
                 edges: list[tuple[str, str]],
                 masked_key: str,
                 wrong: str) -> None:
        """
        ========================================================================
         Init with Topic, the diagram's nodes / edges, the masked node's key,
         and the wrong option. The correct Answer is the masked node's label.
        ========================================================================
        """
        masked = QuestionDiagram._find(nodes=nodes, key=masked_key)
        text = f'[{topic}] Which label fills the missing node?'
        QuestionOptions.__init__(self, text=text,
                                 answer=masked.label, wrong=wrong)
        self._topic = topic
        self._nodes = nodes
        self._edges = edges
        self._masked_key = masked_key

    @staticmethod
    def _find(nodes: list[DiagramNode], key: str) -> DiagramNode:
        """
        ========================================================================
         Return the node with the given key (raises if none).
        ========================================================================
        """
        for node in nodes:
            if node.key == key:
                return node
        raise ValueError(f'No diagram node with key {key!r}')

    @property
    def topic(self) -> str:
        """
        ========================================================================
         Return the Topic of the diagram.
        ========================================================================
        """
        return self._topic

    @property
    def nodes(self) -> list[DiagramNode]:
        """
        ========================================================================
         Return the diagram's nodes (boxes).
        ========================================================================
        """
        return self._nodes

    @property
    def edges(self) -> list[tuple[str, str]]:
        """
        ========================================================================
         Return the diagram's directed edges (src_key -> dst_key).
        ========================================================================
        """
        return self._edges

    @property
    def masked_key(self) -> str:
        """
        ========================================================================
         Return the key of the masked node (the one the student guesses).
        ========================================================================
        """
        return self._masked_key

    def to_scene(self,
                 reveal: Reveal = Reveal.MASKED,
                 options: list[str] | None = None) -> 'Window':
        """
        ========================================================================
         Build the f_gui scene (a Window card) for this question.
        ========================================================================
         `options` lets the caller pin the (otherwise shuffled) option order,
         so a MASKED card and its REVEALED answer key stay consistent.
        ========================================================================
        """
        from f_quiz.question_diagram import _scene
        return _scene.card(q=self, reveal=reveal, options=options)

    def to_html(self,
                path: str,
                reveal: Reveal = Reveal.MASKED,
                options: list[str] | None = None) -> None:
        """
        ========================================================================
         Render the question's scene to a self-contained HTML file.
        ========================================================================
        """
        from f_quiz.question_diagram import _scene
        _scene.to_html(q=self, path=path, reveal=reveal, options=options)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR representation of the QuestionDiagram.
        ========================================================================
        """
        return (f'{self._topic} [{len(self._nodes)} nodes] '
                f'-> {self._answer} | {self._wrong}')
