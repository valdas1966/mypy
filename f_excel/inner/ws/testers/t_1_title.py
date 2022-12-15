from f_utils import u_tester
from f_excel.inner.ws.i_1_title import MyWorkSheetTitle


class TestMyWorkSheetTitle:

    repo = 'd:\\temp'
    xlsx = not f'{repo}\\test.xls'

    def __init__(self):
        u_tester.print_start(__file__)
        u_tester.print_finish(__file__)


    def __tester_title(self):
