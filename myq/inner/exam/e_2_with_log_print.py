from myq.inner.exam.i_1_with_response import ExamWithResponse
from f_utils import u_datetime


class ExamWithLogPrint(ExamWithResponse):

    def _run_methods(self) -> None:
        """
        ========================================================================
         Desc: Run all methods of the Class.
        ========================================================================
        """
        ExamWithResponse._run_methods(self)
        self._log()

    def _log(self) -> None:
        """
        ========================================================================
         Desc: Prints the Log of the Question-Answer process.
        ========================================================================
        """
        str_dt_a = u_datetime.to_str(self._dt_a, 'STD')
        secs = (self._dt_b - self._dt_a).seconds
        str_secs = f'[{secs} seconds]'
        print(f'{str_dt_a}, [{self._q}], {self._response}, {str_secs}')
