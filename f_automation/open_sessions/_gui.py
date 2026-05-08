"""
============================================================================
 Tkinter GUI - button to open Claude sessions in tabs.
============================================================================
"""
import tkinter as tk
from tkinter import messagebox, ttk

from f_automation.open_sessions.main import OpenSessions


class App:
    """
    ============================================================================
     App - Tkinter GUI for launching Claude sessions.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Build the root window.
        ========================================================================
        """
        self._root = tk.Tk()
        self._root.title('Open Claude Sessions')
        self._root.geometry('380x320')
        self._opener = OpenSessions.Factory.a()
        self._txt: tk.Text | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        """
        ========================================================================
         Lay out widgets: label, multi-line entry, Launch button.
        ========================================================================
        """
        ttk.Label(
            self._root,
            text='Session names (one per line):',
        ).pack(padx=10, pady=(10, 4), anchor='w')
        self._txt = tk.Text(self._root, height=10)
        self._txt.pack(padx=10, pady=4, fill='both', expand=True)
        self._txt.focus_set()
        ttk.Button(
            self._root,
            text='Launch',
            command=self._on_launch,
        ).pack(padx=10, pady=10)
        self._root.bind('<Control-Return>',
                        lambda _e: self._on_launch())

    def _on_launch(self) -> None:
        """
        ========================================================================
         Read names, validate, open tabs, close window.
        ========================================================================
        """
        raw = self._txt.get('1.0', 'end').strip()
        names = [
            line.strip()
            for line in raw.splitlines()
            if line.strip()
        ]
        if not names:
            return
        try:
            self._opener.open(names=names)
            self._root.destroy()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def run(self) -> None:
        """
        ========================================================================
         Enter the Tk mainloop.
        ========================================================================
        """
        self._root.mainloop()


if __name__ == '__main__':
    App().run()
