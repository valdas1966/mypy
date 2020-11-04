import pandas as pd
from f_ds import u_plotly
from f_utils import u_tester


class TestPlotly:

    def __init__(self):
        u_tester.print_start(__file__)
        TestPlotly.__tester_bar()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_bar():
        df = pd.DataFrame({'x': [1,2,3,4,5], 'y':[1,2,3,2,1]})
        u_plotly.bar(df=df, col_x='x', col_y='y', title='Test Bar')


if __name__ == '__main__':
    TestPlotly()
