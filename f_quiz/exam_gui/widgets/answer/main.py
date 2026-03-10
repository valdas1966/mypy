import tkinter as tk
from typing import Callable


class WidgetAnswer(tk.Frame):
    """
    ========================================================================
     Widget for user Answer input.
    ========================================================================
    """

    Factory: type = None

    def __init__(self, master: tk.Widget) -> None:
        """
        ====================================================================
         Init with a parent Widget.
        ====================================================================
        """
        super().__init__(master=master, bg='white')
        self._entry = tk.Entry(self,
                               font=('Arial', 30, 'bold'),
                               justify='center',
                               width=25)
        self._entry.pack(pady=20)

    @property
    def text(self) -> str:
        """
        ====================================================================
         Return the current text in the Entry.
        ====================================================================
        """
        return self._entry.get().strip()

    def clear(self) -> None:
        """
        ====================================================================
         Clear the Entry.
        ====================================================================
        """
        self._entry.delete(0, tk.END)

    def focus(self) -> None:
        """
        ====================================================================
         Set focus to the Entry.
        ====================================================================
        """
        self._entry.focus_set()

    def bind_enter(self, callback: Callable) -> None:
        """
        ====================================================================
         Bind Enter key to a callback.
        ====================================================================
        """
        self._entry.bind('<Return>', callback)
