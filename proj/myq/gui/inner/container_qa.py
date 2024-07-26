from typing import Callable
from f_gui.pyqt.container import Container
from f_gui.pyqt.widget_text import WidgetText
from f_gui.pyqt.widgets.label import Label
from f_gui.pyqt.widgets.text_box import TextBox


class ContainerQA(Container):
    """
    ============================================================================
     Container for Question-Label and Answer-TextBox.
    ============================================================================
    """

    def __init__(self,
                 question_first: str,
                 on_enter: Callable[[str], None]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Container.__init__(self, name='QA')
        self._question = self._create_question(question_first)
        self._answer = self._create_answer(on_enter)
        self.add(self._question)
        self.add(self._answer)

    def update(self, question: str) -> None:
        """
        ========================================================================
         Set new question (update Question-Text and clear TextBox).
        ========================================================================
        """
        self._question.text = question
        self._answer.text = str()

    def _create_question(self, question_first: str) -> Label:
        """
        ========================================================================
         Create Question-Label.
        ========================================================================
        """
        question = Label(name='Question')
        self._set_common_params(widget=question)
        question.text = question_first
        question.font.size = 48
        question.position.relative = (0.0, 0.0, 1.0, 0.4)
        return question

    def _create_answer(self, on_enter: Callable[[str], None]) -> TextBox:
        """
        ========================================================================
         Create Answer-TextBox.
        ========================================================================
        """
        answer = TextBox('Answer')
        self._set_common_params(widget=answer)
        answer.set_on_enter(callback=on_enter)
        answer.position.relative = (0.0, 0.6, 1.0, 0.4)
        return answer

    def _set_common_params(self, widget: WidgetText) -> None:
        """
        ========================================================================
         Set common parameters for Question-Label and Answer-TextBox.
        ========================================================================
        """
        widget.background = 'white'
        widget.font.family = 'heebo'
        widget.font.is_bold = True
        widget.font.size = 48
