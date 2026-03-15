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
        super().__init__(master=master, bg='#1e1e2e')
        self._entry = tk.Entry(self,
                               font=('Arial', 54, 'bold'),
                               justify='center',
                               width=25,
                               bg='#313244',
                               fg='white',
                               insertbackground='white',
                               relief='flat',
                               highlightthickness=2,
                               highlightcolor='#89b4fa',
                               highlightbackground='#45475a')
        self._entry.pack(pady=20, ipady=20)

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
