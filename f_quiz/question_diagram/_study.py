"""Study: render QuestionDiagram cards (question + answer key) to HTML.

Builds the f_gui scene for each preset and writes two cards per question —
the MASKED state (what the student sees) and the REVEALED state (answer
key). The option order is pinned so the two cards stay consistent.

Run:  python -m f_quiz.question_diagram._study
      (then open diagram_argument_q.html / _a.html, diagram_modus_q.html / _a.html)
"""
from f_quiz.question_diagram.main import Reveal
from f_quiz.question_diagram._factory import Factory


def render(q, stem: str) -> None:
    opts = q.options                       # pin order across both cards
    q.to_html(path=f'{stem}_q.html', reveal=Reveal.MASKED, options=opts)
    q.to_html(path=f'{stem}_a.html', reveal=Reveal.REVEALED, options=opts)
    print(f'wrote {stem}_q.html / {stem}_a.html')


render(Factory.argument_anatomy(), 'diagram_argument')
render(Factory.modus_ponens(), 'diagram_modus')
