from f_abstract.operation import Operation
from f_abstract.process_tolerant import ProcessTolerant


folder = 'd:\\temp\\study\\log'
header = ['state', 'status', 'dt_start', 'dt_finish', 'secs', 'title',
          'e_msg', 'c', 'b', 'list']

class Op(Operation):
    pass

class P(ProcessTolerant):
    def _pre_run(self) -> None:
        self._create_logger_csv(folder=folder, name=self.title, header=header)
        super()._pre_run()
    def _set_ops(self) -> None:
        self._ops = [Op]*3
    def _set_arg_ops(self) -> None:
        self._arg_ops = [{'list': i} for i in range(3)]

P(b=2)