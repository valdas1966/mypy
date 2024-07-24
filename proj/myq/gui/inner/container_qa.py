from typing import Callable
from f_gui.pyqt.container import Container
from f_gui.pyqt.widget_text import WidgetText
from f_gui.pyqt.widgets.label import Label
from f_gui.pyqt.widgets.text_box import TextBox


class ContainerQA(Container):

    def __init__(self, on_enter: Callable[[], None]) -> None:
        Container.__init__(self, name='QA')
        q = self._create_question()
        a = self._create_answer(on_enter)
        self.add(q)
        self.add(a)

    def _create_question(self) -> Label:
        question = Label('Question')
        self._set_common_params(widget=question)
        question.font.size = 48
        question.text = 'Hello'
        question.position.relative = (0.0, 0.0, 1.0, 0.4)
        return question

    def _create_answer(self, on_enter: Callable[[], None]) -> TextBox:
        answer = TextBox('Answer')
        self._set_common_params(widget=answer)
        answer.set_on_enter(callback=on_enter)
        answer.position.relative = (0.0, 0.6, 1.0, 0.4)
        return answer

    def _set_common_params(self, widget: WidgetText) -> None:
        widget.background = 'white'
        widget.font.family = 'heebo'
        widget.font.is_bold = True
        widget.font.size = 48
