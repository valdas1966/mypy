from typing import Callable
from f_gui.pyqt.container import Container
from f_gui.pyqt.widget_text import WidgetText
from f_gui.pyqt.widgets.label import Label
from f_gui.pyqt.widgets.text_box import TextBox


class ContainerQA(Container):

    def __init__(self, on_enter: Callable[[], None]) -> None:
        Container.__init__(self, name='QA')
        self.background = 'green'
        q = self._create_question()
        a = self._create_answer(on_enter)
        self.add(q, 0, 0, 100, 40)
        self.add(a, 0, 60, 100, 40)

    @staticmethod
    def _create_question() -> Label:
        question = Label('Question')
        ContainerQA._set_common_params(widget=question)
        question.font.size = 48
        question.text = 'Hello'
        return question

    @staticmethod
    def _create_answer(on_enter: Callable[[], None]) -> TextBox:
        answer = TextBox('Answer')
        ContainerQA._set_common_params(widget=answer)
        answer.set_on_enter(callback=on_enter)
        return answer

    @staticmethod
    def _set_common_params(widget: WidgetText) -> None:
        widget.background = 'white'
        widget.font.family = 'heebo'
        widget.font.is_bold = True
        widget.font.size = 48
