from typing import Callable
from f_gui.pyqt.container import Container
from f_gui.pyqt.widget_text import WidgetText
from f_gui.pyqt.widgets.label import Label
from f_gui.pyqt.widgets.text_box import TextBox
from proj.myq.question.i_1_text import QuestionText
from f_utils.dtypes.u_str import UStr as u_str


class ContainerQA(Container):
    """
    ============================================================================
     Container for Question-Label and Answer-TextBox.
    ============================================================================
    """

    COMMON_LEFT = 0.0
    COMMON_WIDTH = 1.0
    HEIGHT_QUESTION = 0.37
    HEIGHT_MASK = 0.15
    HEIGHT_ANSWER = 0.28
    HEIGHT_DELTA = 0.1

    def __init__(self,
                 question_first: QuestionText,
                 on_enter: Callable[[str], None]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Container.__init__(self, name='QA')
        self._question = self._create_question()
        self._mask = self._create_mask()
        self._answer = self._create_answer(on_enter)
        self.update(question=question_first)
        self.add(self._question)
        self.add(self._mask)
        self.add(self._answer)

    def update(self, question: QuestionText) -> None:
        """
        ========================================================================
         Set new question (update Question-Text and clear TextBox).
        ========================================================================
        """
        self._question.text = question.text
        self._mask.text = u_str.mask.full(question.answer)
        self._answer.text = str()

    def _create_question(self) -> Label:
        """
        ========================================================================
         Create Question-Label.
        ========================================================================
        """
        question = Label(name='Question')
        self._set_common_params(widget=question)
        question.position.relative = (self.COMMON_LEFT,
                                      0.0,
                                      self.COMMON_WIDTH,
                                      self.HEIGHT_QUESTION)
        return question

    def _create_mask(self) -> Label:
        """
        ========================================================================
         Create Answer-Mask.
        ========================================================================
        """
        mask = Label(name='Mask')
        self._set_common_params(widget=mask)
        mask.position.relative = (self.COMMON_LEFT,
                                  self.HEIGHT_QUESTION + self.HEIGHT_DELTA,
                                  self.COMMON_WIDTH,
                                  self.HEIGHT_MASK)
        mask.background = 'lightgray'
        mask.font.size = 32
        return mask

    def _create_answer(self, on_enter: Callable[[str], None]) -> TextBox:
        """
        ========================================================================
         Create Answer-TextBox.
        ========================================================================
        """
        answer = TextBox('Answer')
        self._set_common_params(widget=answer)
        answer.set_on_enter(callback=on_enter)
        answer.position.relative = (self.COMMON_LEFT,
                                    self.HEIGHT_QUESTION + self.HEIGHT_MASK +
                                    self.HEIGHT_DELTA*2,
                                    self.COMMON_WIDTH,
                                    self.HEIGHT_ANSWER)
        print(answer.alignment.vertical, answer.alignment.horizontal)
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
        widget.font.size = 32
