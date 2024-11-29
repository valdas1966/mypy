from f_core.operation import Operation


folder = 'd:\\temp\\study\\log'
name = 'op'
header = ['list', 'b', 'c']


class Op(Operation):

    def _pre_run(self) -> None:
        self._create_logger_csv(folder=folder, name=self.title, header=header)
        super()._pre_run()


Op(a=1, b=2, d=4)
