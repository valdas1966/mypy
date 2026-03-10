import tkinter as tk


class WidgetQuestion(tk.Frame):
    """
    ========================================================================
     Widget for displaying the Question text.
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
        # Counter label
        self._label_counter = tk.Label(self,
                                       font=('Arial', 24),
                                       fg='#888888',
                                       bg='white')
        self._label_counter.pack(pady=(20, 0))
        # Question text label
        self._label_text = tk.Label(self,
                                    font=('Arial', 36, 'bold'),
                                    bg='white',
                                    wraplength=900)
        self._label_text.pack(pady=20)

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
