from f_quiz.question_diagram.main import QuestionDiagram, DiagramNode, Reveal
from f_gui.elements.i_1_label.main import Label
from f_ds.geometry.bounds import Bounds


def _q() -> QuestionDiagram:
    """
    ========================================================================
     A minimal two-node diagram: a -> b, with b masked (answer 'Yes').
    ========================================================================
    """
    return QuestionDiagram(
        topic='T',
        nodes=[
            DiagramNode(key='a',
                        bounds=Bounds(top=10, left=10, bottom=30, right=40),
                        label='Cause'),
            DiagramNode(key='b',
                        bounds=Bounds(top=60, left=10, bottom=80, right=40),
                        label='Yes'),
        ],
        edges=[('a', 'b')],
        masked_key='b',
        wrong='No',
    )


def test_answer_is_masked_label() -> None:
    """
    ========================================================================
     Test that the correct answer is the masked node's label.
    ========================================================================
    """
    assert _q().answer == 'Yes'


def test_options_contain_answer_and_wrong() -> None:
    """
    ========================================================================
     Test that options are the answer + the wrong distractor.
    ========================================================================
    """
    assert set(_q().options) == {'Yes', 'No'}


def test_spec_stored() -> None:
    """
    ========================================================================
     Test that nodes / edges / masked_key are stored.
    ========================================================================
    """
    q = _q()
    assert [n.key for n in q.nodes] == ['a', 'b']
    assert q.edges == [('a', 'b')]
    assert q.masked_key == 'b'


def test_unknown_masked_key_raises() -> None:
    """
    ========================================================================
     Test that an unknown masked_key raises ValueError.
    ========================================================================
    """
    try:
        QuestionDiagram(topic='T', nodes=[], edges=[], masked_key='x',
                        wrong='No')
        assert False, 'expected ValueError'
    except ValueError:
        pass


def _masked_text(q: QuestionDiagram, reveal: Reveal) -> str:
    """
    ========================================================================
     The rendered text of the masked node's Label in the given state.
    ========================================================================
    """
    diagram = q.to_scene(reveal=reveal).children[1]     # [prompt, diagram, ...]
    mb = QuestionDiagram._find(nodes=q.nodes, key=q.masked_key).bounds
    for child in diagram.children:
        if isinstance(child, Label) and child.bounds.to_tuple() == mb.to_tuple():
            return child.text
    raise AssertionError('masked node Label not found')


def test_masked_shows_question_mark() -> None:
    """
    ========================================================================
     Test that the masked node renders '?' in the MASKED state.
    ========================================================================
    """
    assert _masked_text(q=_q(), reveal=Reveal.MASKED) == '?'


def test_revealed_shows_answer() -> None:
    """
    ========================================================================
     Test that the masked node renders the answer in the REVEALED state.
    ========================================================================
    """
    assert _masked_text(q=_q(), reveal=Reveal.REVEALED) == 'Yes'


def test_scene_child_count() -> None:
    """
    ========================================================================
     Test the card structure: prompt + diagram + two options = 4 children;
     the diagram holds one Label per node plus one Connector per edge.
    ========================================================================
    """
    q = _q()
    win = q.to_scene()
    assert len(win.children) == 4
    diagram = win.children[1]
    assert len(diagram.children) == len(q.nodes) + len(q.edges)


def test_factory_argument_anatomy() -> None:
    """
    ========================================================================
     Test the argument_anatomy preset's answer.
    ========================================================================
    """
    assert QuestionDiagram.Factory.argument_anatomy().answer == 'Conclusion'
