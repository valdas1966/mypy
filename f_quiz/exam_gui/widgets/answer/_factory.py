import tkinter as tk

from f_quiz.exam_gui.widgets.answer.main import WidgetAnswer


class Factory:
    """
    ========================================================================
     Factory for WidgetAnswer.
    ========================================================================
    """

    @staticmethod
    def gen(master: tk.Widget) -> WidgetAnswer:
        """
        ====================================================================
         Create a WidgetAnswer with the given master.
        ====================================================================
        """
        return WidgetAnswer(master=master)
