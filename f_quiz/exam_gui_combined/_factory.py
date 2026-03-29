from f_quiz.exam_gui_combined.main import ExamGuiCombined
from f_quiz.question import Question
from f_quiz.question_options import QuestionOptions
from f_quiz.loaders.u_gsheet import load, load_options, load_yes_no
import random


class Factory:
    """
    ========================================================================
     Factory for ExamGuiCombined.
    ========================================================================
    """

    @staticmethod
    def test() -> ExamGuiCombined:
        """
        ====================================================================
         Create with two text + two options Questions.
        ====================================================================
        """
        questions: list[Question] = [
            Question.Factory.capital_of_france(),
            QuestionOptions.Factory.logic(),
            Question.Factory.capital_of_germany(),
            QuestionOptions.Factory.formal()
        ]
        return ExamGuiCombined(questions=questions)

    @staticmethod
    def combined(is_random: bool = True,
                 n_questions: int | None = None
                 ) -> ExamGuiCombined:
        """
        ====================================================================
         Create from Hebrew + Options + YesNo Google Sheets.
         Distribution: 70% YesNo, 30% Options, 10% Hebrew.
        ====================================================================
        """
        pool_hebrew = load(sheet_name='Hebrew')
        pool_options = load_options()
        pool_yes_no = load_yes_no()
        questions = _sample_by_ratio(
            pools=[(pool_yes_no, 0.7),
                   (pool_options, 0.2),
                   (pool_hebrew, 0.1)],
            n=n_questions)
        return ExamGuiCombined(questions=questions,
                               is_random=is_random,
                               n_questions=None)


def _sample_by_ratio(pools: list[tuple[list[Question], float]],
                     n: int | None) -> list[Question]:
    """
    ========================================================================
     Sample questions from pools according to given ratios.
     If n is None, use all available questions.
    ========================================================================
    """
    if n is None:
        questions = []
        for pool, _ in pools:
            questions += pool
        return questions
    # Shuffle each pool
    for pool, _ in pools:
        random.shuffle(pool)
    # Calculate counts per pool
    counts = _split_counts(n=n, ratios=[r for _, r in pools])
    # Sample from each pool
    questions = []
    for (pool, _), count in zip(pools, counts):
        questions += pool[:count]
    return questions


def _split_counts(n: int, ratios: list[float]) -> list[int]:
    """
    ========================================================================
     Split n into integer counts matching the given ratios.
     Remainders are distributed to the largest-ratio pools first.
    ========================================================================
    """
    raw = [r * n for r in ratios]
    counts = [int(c) for c in raw]
    remainder = n - sum(counts)
    # Distribute remainder by largest fractional part
    fracs = [(raw[i] - counts[i], i) for i in range(len(counts))]
    fracs.sort(reverse=True)
    for j in range(remainder):
        counts[fracs[j][1]] += 1
    return counts
