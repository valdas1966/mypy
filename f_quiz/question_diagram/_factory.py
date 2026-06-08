from f_quiz.question_diagram.main import QuestionDiagram, DiagramNode
from f_ds.geometry.bounds import Bounds


class Factory:
    """
    ============================================================================
     Factory for QuestionDiagram — the f_gui-backed visual questions.
    ============================================================================
     Mirrors the topics of the (Drive-SVG) QuestionVisual factory, but the
     diagram is built from f_gui elements instead of a hand-authored SVG.
     Node bounds are 0-100 relative to the diagram region.
    ============================================================================
    """

    @staticmethod
    def argument_anatomy() -> QuestionDiagram:
        """
        ========================================================================
         Two premises converging on a masked Conclusion (vs Premise).
        ========================================================================
        """
        return QuestionDiagram(
            topic='Argument Anatomy',
            nodes=[
                DiagramNode(key='p1',
                            bounds=Bounds(top=10, left=6, bottom=34, right=40),
                            label='Premise 1'),
                DiagramNode(key='p2',
                            bounds=Bounds(top=10, left=60, bottom=34, right=94),
                            label='Premise 2'),
                DiagramNode(key='c',
                            bounds=Bounds(top=62, left=33, bottom=88, right=67),
                            label='Conclusion'),
            ],
            edges=[('p1', 'c'), ('p2', 'c')],
            masked_key='c',
            wrong='Premise',
        )

    @staticmethod
    def modus_ponens() -> QuestionDiagram:
        """
        ========================================================================
         'If P then Q' + 'P' entailing a masked Q (vs P).
        ========================================================================
        """
        return QuestionDiagram(
            topic='Modus Ponens',
            nodes=[
                DiagramNode(key='cond',
                            bounds=Bounds(top=8, left=20, bottom=30, right=80),
                            label='If P then Q'),
                DiagramNode(key='p',
                            bounds=Bounds(top=40, left=33, bottom=60, right=67),
                            label='P'),
                DiagramNode(key='q',
                            bounds=Bounds(top=70, left=33, bottom=92, right=67),
                            label='Q'),
            ],
            edges=[('cond', 'q'), ('p', 'q')],
            masked_key='q',
            wrong='P',
        )
