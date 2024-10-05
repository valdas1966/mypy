from typing import Callable
from f_gui.pyqt.app import App
from f_gui.pyqt.widgets.msg_box import MsgBox
from proj.myq.questions.i_2_mask import QuestionMask
from proj.myq.gui.inner.container_qa import ContainerQA


class AppQA(App):
    """
    ============================================================================
     Gui-App for Question-Answer screen.
    ============================================================================
    """

    def __init__(self,
                 question_first: QuestionMask,
                 on_enter: Callable[[str], None]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        App.__init__(self, name='Myq')
        self.background = 'black'
        self._con_qa = ContainerQA(question_first=question_first,
                                   on_enter=on_enter)
        self._con_qa.position.relative = (0.05, 0.25, 0.9, 0.45)
        self.add(self._con_qa)

    def update(self, question: QuestionMask) -> None:
        """
        ========================================================================
         Update the Q/A Container (new Question and empty Answer).
        ========================================================================
        """
        self._con_qa.update(question)

    def msg_box(self, text: str) -> None:
        """
        ========================================================================
         Show MsgBox with Title and Text.
        ========================================================================
        """
        MsgBox(text=text)
