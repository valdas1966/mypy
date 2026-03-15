import tkinter as tk

from f_quiz.question.main import Question
from f_quiz.exam_gui.runner.main import ExamRunner
from f_quiz.exam_gui.widgets.question.main import WidgetQuestion
from f_quiz.exam_gui.widgets.answer.main import WidgetAnswer
from f_quiz.exam_gui.widgets.status.main import WidgetStatus


class ExamGui:
    """
    ========================================================================
     GUI Exam Application.
     Displays Questions and accepts Answers via tkinter.
    ========================================================================
    """

    Factory: type = None

    def __init__(self,
                 questions: list[Question],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None:
        """
        ====================================================================
         Init with Questions and optional configuration.
        ====================================================================
        """
        self._runner = ExamRunner(questions=questions,
                                  is_random=is_random,
                                  n_questions=n_questions)
        self._root = tk.Tk()
        self._root.title('Exam')
        self._root.attributes('-fullscreen', True)
        self._root.configure(bg='#1e1e2e')
        # Escape to exit fullscreen
        self._root.bind('<Escape>', lambda e: self._root.destroy())
        # Widgets
        self._w_question = WidgetQuestion(master=self._root)
        self._w_question.pack(fill=tk.X, padx=80, pady=(60, 20))
        self._w_answer = WidgetAnswer(master=self._root)
        self._w_answer.pack(padx=80, pady=20)
        self._w_status = WidgetStatus(master=self._root)
        self._w_status.pack(fill=tk.X, padx=80, pady=20)
        # Bind Enter
        self._w_answer.bind_enter(callback=self._on_enter)
        # Show first question
        self._show_question()

    def run(self) -> None:
        """
        ====================================================================
         Run the GUI application.
        ====================================================================
        """
        self._root.mainloop()

    def _on_enter(self, event: tk.Event) -> None:
        """
        ====================================================================
         Handle Enter key press.
        ====================================================================
        """
        if self._runner.is_finished:
            self._root.destroy()
            return
        q = self._runner.current
        is_correct = self._runner.check(
            answer=self._w_answer.text
        )
        # Update status
        if is_correct:
            self._w_status.set_correct()
            self._w_status.set_score(score=self._runner.score,
                                     total=self._runner.total)
            # Next question or finish
            if self._runner.is_finished:
                self._w_status.set_finished(
                    score=self._runner.score,
                    total=self._runner.total
                )
                self._w_answer.clear()
            else:
                self._show_question()
        else:
            # Show correct answer, re-ask same question
            self._w_status.set_wrong(answer=q.answer)
            self._w_answer.clear()
            self._w_answer.focus()

    def _show_question(self) -> None:
        """
        ====================================================================
         Display the current Question.
        ====================================================================
        """
        q = self._runner.current
        self._w_question.set_question(number=self._runner.number,
                                      total=self._runner.total,
                                      text=q.text)
        self._w_answer.clear()
        self._w_answer.focus()
