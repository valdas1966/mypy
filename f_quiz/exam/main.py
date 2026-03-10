import random

from f_quiz.question.main import Question


class Exam:
    """
    ========================================================================
     Interactive Quiz Exam.
     Prompts the User with Questions and checks Answers.
    ========================================================================
    """

    Factory: type = None

    def __init__(self,
                 questions: list[Question],
                 is_random: bool = False,
                 n_questions: int | None = None) -> None:
        """
        ====================================================================
         Init with a list of Questions.
        ====================================================================
        """
        self._questions = questions
        self._is_random = is_random
        self._n_questions = n_questions

    @property
    def questions(self) -> list[Question]:
        """
        ====================================================================
         Return the list of Questions.
        ====================================================================
        """
        return self._questions

    def run(self) -> None:
        """
        ====================================================================
         Run the Exam interactively in the terminal.
        ====================================================================
        """
        # Prepare questions
        qs = self._prepare_questions()
        correct = 0
        total = len(qs)
        for i, q in enumerate(qs, start=1):
            print(f'\nQuestion {i}/{total}: {q.text}')
            user_answer = input('Your answer: ').strip()
            if user_answer.lower() == q.answer.lower():
                print('Correct!')
                correct += 1
            else:
                print(f'Wrong! The correct answer is: {q.answer}')
        print(f'\nResults: {correct}/{total}')

    def _prepare_questions(self) -> list[Question]:
        """
        ====================================================================
         Prepare Questions for the Exam (shuffle and/or limit).
        ====================================================================
        """
        qs = list(self._questions)
        if self._is_random:
            random.shuffle(qs)
        if self._n_questions is not None:
            qs = qs[:self._n_questions]
        return qs
