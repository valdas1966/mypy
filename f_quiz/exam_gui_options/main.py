import tkinter as tk

from f_quiz.question_options.main import QuestionOptions
from f_quiz.exam_gui.runner.main import ExamRunner
from f_quiz.exam_gui.widgets.question.main import WidgetQuestion
from f_quiz.exam_gui.widgets.options.main import WidgetOptions
from f_quiz.exam_gui.widgets.status.main import WidgetStatus


class ExamGuiOptions:
    """
    ========================================================================
     GUI Exam for two-option Questions.
     User presses 1 or 2 to choose the correct Answer.
    ========================================================================
    """

    Factory: type = None

    def __init__(self,
                 questions: list[QuestionOptions],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None:
        """
        ====================================================================
         Init with QuestionOptions and optional configuration.
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
        self._w_options = WidgetOptions(master=self._root)
        self._w_options.pack(fill=tk.X, padx=80, pady=20)
        self._w_status = WidgetStatus(master=self._root)
        self._w_status.pack(fill=tk.X, padx=80, pady=20)
        # Bind keys 1 and 2
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

    def _on_key(self, key: int) -> None:
        """
        ====================================================================
         Handle key press (1 or 2).
        ====================================================================
        """
        if self._runner.is_finished:
            self._root.destroy()
            return
        answer = self._w_options.get(key=key)
        is_correct = self._runner.check(answer=answer)
        if is_correct:
            self._w_status.set_correct()
            self._w_status.set_score(score=self._runner.score,
                                     total=self._runner.total)
            if self._runner.is_finished:
                self._finish()
            else:
                self._show_question()
        else:
            self._w_status.set_wrong(
                answer=self._runner.current.answer
            )
            self._show_question()

    def _show_question(self) -> None:
        """
        ====================================================================
         Display the current Question with Options.
        ====================================================================
        """
        q: QuestionOptions = self._runner.current
        self._w_question.set_question(number=self._runner.number,
                                      total=self._runner.total,
                                      text=q.text)
        self._w_options.set_options(options=q.options)

    def _finish(self) -> None:
        """
        ====================================================================
         Display the final results.
        ====================================================================
        """
        self._w_status.set_finished(score=self._runner.score,
                                    total=self._runner.total)
        self._w_options.clear()
