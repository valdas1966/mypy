import tkinter as tk

from f_quiz.question.main import Question
from f_quiz.question_options.main import QuestionOptions
from f_quiz.exam_gui.runner.main import ExamRunner
from f_quiz.exam_gui.widgets.question.main import WidgetQuestion
from f_quiz.exam_gui.widgets.answer.main import WidgetAnswer
from f_quiz.exam_gui.widgets.options.main import WidgetOptions
from f_quiz.exam_gui.widgets.status.main import WidgetStatus


class ExamGuiCombined:
    """
    ========================================================================
     Combined GUI Exam for mixed Question types.
     Text-input Questions use Enter key.
     Two-option Questions use 1/2 keys.
    ========================================================================
    """

    Factory: type = None

    def __init__(self,
                 questions: list[Question],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None:
        """
        ====================================================================
         Init with mixed Questions and optional configuration.
        ====================================================================
        """
        self._runner = ExamRunner(questions=questions,
                                  is_random=is_random,
                                  n_questions=n_questions)
        self._root = tk.Tk()
        self._root.title('Exam')
        self._root.attributes('-fullscreen', True)
        self._root.configure(bg='#1e1e2e')
        # Escape to exit
        self._root.bind('<Escape>',
                        lambda e: self._root.destroy())
        # Widgets
        self._w_question = WidgetQuestion(master=self._root,
                                          font_size=44)
        self._w_question.pack(fill=tk.X, padx=80, pady=(60, 20))
        # Text-input widget
        self._w_answer = WidgetAnswer(master=self._root)
        # Options widget
        self._w_options = WidgetOptions(master=self._root)
        # Status widget
        self._w_status = WidgetStatus(master=self._root)
        self._w_status.pack(fill=tk.X, padx=80, pady=20)
        # Bind Enter for text-input
        self._w_answer.bind_enter(callback=self._on_enter)
        # Bind 1/2 for options
        self._root.bind('1', lambda e: self._on_key(key=1))
        self._root.bind('2', lambda e: self._on_key(key=2))
        # Show first question
        self._show_question()

    def run(self) -> None:
        """
        ====================================================================
         Run the GUI application.
        ====================================================================
        """
        self._root.mainloop()

    def _is_options(self) -> bool:
        """
        ====================================================================
         Return True if current Question is QuestionOptions.
        ====================================================================
        """
        return isinstance(self._runner.current, QuestionOptions)

    def _show_question(self) -> None:
        """
        ====================================================================
         Display the current Question with the appropriate widget.
        ====================================================================
        """
        q = self._runner.current
        self._w_question.set_question(number=self._runner.number,
                                      total=self._runner.total,
                                      text=q.text)
        if self._is_options():
            # Hide answer, show options
            self._w_answer.pack_forget()
            self._w_options.pack(fill=tk.X, padx=80, pady=20)
            self._w_options.set_options(options=q.options)
        else:
            # Hide options, show answer
            self._w_options.pack_forget()
            self._w_answer.pack(padx=80, pady=20)
            self._w_answer.clear()
            self._w_answer.focus()
        # Re-pack status at bottom
        self._w_status.pack_forget()
        self._w_status.pack(fill=tk.X, padx=80, pady=20)

    def _on_enter(self, event: tk.Event) -> None:
        """
        ====================================================================
         Handle Enter key press (text-input Questions).
        ====================================================================
        """
        if self._runner.is_finished or self._is_options():
            return
        q = self._runner.current
        is_correct = self._runner.check(
            answer=self._w_answer.text
        )
        if is_correct:
            self._w_status.set_correct()
            self._w_status.set_score(score=self._runner.score,
                                     total=self._runner.total)
            if self._runner.is_finished:
                self._finish()
            else:
                self._show_question()
        else:
            self._w_status.set_wrong(answer=q.answer)
            self._w_answer.clear()
            self._w_answer.focus()

    def _on_key(self, key: int) -> None:
        """
        ====================================================================
         Handle key press 1 or 2 (option Questions).
        ====================================================================
        """
        if self._runner.is_finished:
            self._root.destroy()
            return
        if not self._is_options():
            return
        q: QuestionOptions = self._runner.current
        answer = self._w_options.get(key=key)
        is_correct = self._runner.check(answer=answer)
        # Find which key has the correct answer
        correct_key = (1 if self._w_options.get(key=1)
                       == q.answer else 2)
        if is_correct:
            self._w_options.highlight_correct(key=key)
            self._w_status.set_correct()
            self._w_status.set_score(score=self._runner.score,
                                     total=self._runner.total)
            if self._runner.is_finished:
                self._root.after(
                    1000,
                    lambda: self._finish()
                )
            else:
                self._root.after(1000,
                                 lambda: self._show_question())
        else:
            self._w_options.highlight_wrong(key=key)
            self._w_options.highlight_correct(key=correct_key)
            self._w_status.set_wrong(answer=q.answer)
            self._root.after(
                2000,
                lambda: self._show_question()
            )

    def _finish(self) -> None:
        """
        ====================================================================
         Display the final results.
        ====================================================================
        """
        self._w_answer.pack_forget()
        self._w_options.pack_forget()
        self._w_status.set_finished(score=self._runner.score,
                                    total=self._runner.total)
