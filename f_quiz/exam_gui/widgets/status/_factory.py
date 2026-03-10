import tkinter as tk

from f_quiz.exam_gui.widgets.status.main import WidgetStatus


class Factory:
    """
    ========================================================================
     Factory for WidgetStatus.
    ========================================================================
    """

    @staticmethod
    def gen(master: tk.Widget) -> WidgetStatus:
        """
        ====================================================================
         Create a WidgetStatus with the given master.
        ====================================================================
        """
        return WidgetStatus(master=master)
