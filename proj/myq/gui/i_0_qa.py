from typing import Callable
from f_gui.pyqt.app import App
from proj.myq.gui.inner.container_qa import ContainerQA


class AppQA(App):
    """
    ============================================================================
     Gui-App for Question-Answer screen.
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
        App.__init__(self, name='Myq')
        self.background = 'black'
        self._con_qa = ContainerQA(question_first=question_first,
                                   on_enter=on_enter)
        self._con_qa.position.relative = (0.1, 0.3, 0.8, 0.4)
        self.add(self._con_qa)

    def update(self, question: str) -> None:
        self._con_qa.update(question)
