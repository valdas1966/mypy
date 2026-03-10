import random

from f_quiz.question.main import Question


class ExamRunner:
    """
    ========================================================================
     Exam Runner - Manages Exam Logic (no GUI).
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
        self._questions_all = questions
        self._is_random = is_random
        self._n_questions = n_questions
        self._questions = self._prepare_questions()
        self._index = 0
        self._score = 0

    @property
    def current(self) -> Question | None:
        """
        ====================================================================
         Return the current Question (or None if finished).
        ====================================================================
        """
        if self.is_finished:
            return None
        return self._questions[self._index]

    @property
    def number(self) -> int:
        """
        ====================================================================
         Return the current Question number (1-based).
        ====================================================================
        """
        return self._index + 1

    @property
    def total(self) -> int:
        """
        ====================================================================
         Return the total number of Questions.
        ====================================================================
        """
        return len(self._questions)

    @property
    def score(self) -> int:
        """
        ====================================================================
         Return the number of correct Answers.
        ====================================================================
        """
        return self._score

    @property
    def is_finished(self) -> bool:
        """
        ====================================================================
         Return True if all Questions have been answered.
        ====================================================================
        """
        return self._index >= len(self._questions)

    def check(self, answer: str) -> bool:
        """
        ====================================================================
         Check the Answer, update score, and advance to next Question.
        ====================================================================
        """
        q = self.current
        is_correct = answer.strip().lower() == q.answer.lower()
        if is_correct:
            self._score += 1
        self._index += 1
        return is_correct

    def _prepare_questions(self) -> list[Question]:
        """
        ====================================================================
         Prepare Questions (shuffle and/or limit).
        ====================================================================
        """
        qs = list(self._questions_all)
        if self._is_random:
            random.shuffle(qs)
        if self._n_questions is not None:
            qs = qs[:self._n_questions]
        return qs
