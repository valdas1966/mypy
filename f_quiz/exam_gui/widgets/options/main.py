import tkinter as tk


class WidgetOptions(tk.Frame):
    """
    ========================================================================
     Widget for displaying two Answer Options.
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
        self._opts: list[str] = []
        self._label_1 = tk.Label(self,
                                 font=('Arial', 48, 'bold'),
                                 fg='white',
                                 bg='#313244',
                                 anchor='center',
                                 padx=40,
                                 pady=20)
        self._label_1.pack(side=tk.LEFT,
                           expand=True,
                           fill=tk.BOTH,
                           padx=(0, 10))
        self._label_2 = tk.Label(self,
                                 font=('Arial', 48, 'bold'),
                                 fg='white',
                                 bg='#313244',
                                 anchor='center',
                                 padx=40,
                                 pady=20)
        self._label_2.pack(side=tk.LEFT,
                           expand=True,
                           fill=tk.BOTH,
                           padx=(10, 0))

    def set_options(self, options: list[str]) -> None:
        """
        ====================================================================
         Display two Options.
        ====================================================================
        """
        self._opts = options
        self._label_1.config(text=f'1.  {options[0]}',
                             bg='#313244', fg='white')
        self._label_2.config(text=f'2.  {options[1]}',
                             bg='#313244', fg='white')

    def get(self, key: int) -> str:
        """
        ====================================================================
         Return the Option text by key (1 or 2).
        ====================================================================
        """
        return self._opts[key - 1]

    def highlight_correct(self, key: int) -> None:
        """
        ====================================================================
         Highlight the correct Option in green.
        ====================================================================
        """
        label = self._label_1 if key == 1 else self._label_2
        label.config(bg='#a6e3a1', fg='#1e1e2e')

    def highlight_wrong(self, key: int) -> None:
        """
        ====================================================================
         Highlight the wrong Option in red.
        ====================================================================
        """
        label = self._label_1 if key == 1 else self._label_2
        label.config(bg='#f38ba8', fg='#1e1e2e')

    def clear(self) -> None:
        """
        ====================================================================
         Reset both Options.
        ====================================================================
        """
        self._label_1.config(text='', bg='#313244', fg='white')
        self._label_2.config(text='', bg='#313244', fg='white')
        self._opts = []
