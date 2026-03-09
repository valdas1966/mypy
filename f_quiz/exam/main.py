from f_quiz.question.main import Question


class Exam:
    """
    ========================================================================
     Interactive Quiz Exam.
     Prompts the User with Questions and checks Answers.
    ========================================================================
    """

    Factory: type = None

    def __init__(self, questions: list[Question]) -> None:
        """
        ====================================================================
         Init with a list of Questions.
        ====================================================================
        """
        self._questions = questions

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
        correct = 0
        total = len(self._questions)
        for i, q in enumerate(self._questions, start=1):
            print(f'\nQuestion {i}/{total}: {q.text}')
            user_answer = input('Your answer: ').strip()
            if user_answer.lower() == q.answer.lower():
                print('Correct!')
                correct += 1
            else:
                print(f'Wrong! The correct answer is: {q.answer}')
        print(f'\nResults: {correct}/{total}')
