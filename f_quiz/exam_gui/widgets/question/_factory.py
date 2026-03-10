import tkinter as tk

from f_quiz.exam_gui.widgets.question.main import WidgetQuestion


class Factory:
    """
    ========================================================================
     Factory for WidgetQuestion.
    ========================================================================
    """

    @staticmethod
    def gen(master: tk.Widget) -> WidgetQuestion:
        """
        ====================================================================
         Create a WidgetQuestion with the given master.
        ====================================================================
        """
        return WidgetQuestion(master=master)
