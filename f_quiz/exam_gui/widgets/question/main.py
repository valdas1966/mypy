import tkinter as tk


class WidgetQuestion(tk.Frame):
    """
    ========================================================================
     Widget for displaying the Question text.
    ========================================================================
    """

    Factory: type = None

    def __init__(self,
                 master: tk.Widget,
                 font_size: int = 64) -> None:
        """
        ====================================================================
         Init with a parent Widget and optional font size.
        ====================================================================
        """
        super().__init__(master=master, bg='#1e1e2e')
        # Counter label
        self._label_counter = tk.Label(self,
                                       font=('Arial', 32),
                                       fg='#6c7086',
                                       bg='#1e1e2e')
        self._label_counter.pack(pady=(20, 0))
        # Question text label
        self._label_text = tk.Label(self,
                                    font=('Arial', font_size, 'bold'),
                                    fg='white',
                                    bg='#1e1e2e',
                                    wraplength=1200)
        self._label_text.pack(pady=(30, 40))

    def set_question(self,
                     number: int,
                     total: int,
                     text: str) -> None:
        """
        ====================================================================
         Update the displayed Question.
        ====================================================================
        """
        self._label_counter.config(
            text=f'Question {number}/{total}'
        )
        self._label_text.config(text=text)
