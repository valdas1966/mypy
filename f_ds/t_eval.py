import pandas as pd
from f_utils import u_tester
from f_ds import u_eval


class TestEval:

    def __init__(self):
        u_tester.print_start(__file__)
        TestEval.__tester_score()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_score():
        df = pd.DataFrame({'true': [10, 10, 10],
                           'false': [20, 20, 20],
                           'pred': [1, 0, 1]})
        score = u_eval.score(df, col_true='true', col_false='false')
        p0 = score == 40
        u_tester.run(p0)


if __name__ == '__main__':
    TestEval()
