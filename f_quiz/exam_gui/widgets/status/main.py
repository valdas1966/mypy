import tkinter as tk


class WidgetStatus(tk.Frame):
    """
    ========================================================================
     Widget for displaying Answer feedback and score.
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
        # Feedback label
        self._label_feedback = tk.Label(self,
                                        font=('Arial', 28, 'bold'),
                                        bg='#1e1e2e',
                                        text='')
        self._label_feedback.pack(pady=10)
        # Score label
        self._label_score = tk.Label(self,
                                     font=('Arial', 22),
                                     fg='#6c7086',
                                     bg='#1e1e2e',
                                     text='')
        self._label_score.pack(pady=10)

    def set_correct(self) -> None:
        """
        ====================================================================
         Display 'Correct!' feedback.
        ====================================================================
        """
        self._label_feedback.config(text='Correct!', fg='#a6e3a1')

    def set_wrong(self, answer: str) -> None:
        """
        ====================================================================
         Display 'Wrong!' feedback with the correct Answer.
        ====================================================================
        """
        self._label_feedback.config(
            text=f'Wrong! Correct answer: {answer}',
            fg='#f38ba8'
        )

    def set_score(self, score: int, total: int) -> None:
        """
        ====================================================================
         Update the score display.
        ====================================================================
        """
        self._label_score.config(text=f'Score: {score}/{total}')

    def set_finished(self, score: int, total: int) -> None:
        """
        ====================================================================
         Display the final results.
        ====================================================================
        """
        self._label_feedback.config(
            text=f'Exam Finished! {score}/{total}',
            fg='#89b4fa',
            font=('Arial', 36, 'bold')
        )
        self._label_score.config(text='')
