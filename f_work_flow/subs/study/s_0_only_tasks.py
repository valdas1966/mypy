from f_work_flow.subs.sub_0_only_tasks import WorkflowOnlyTasks


class WorkFlow(WorkflowOnlyTasks):

    def __init__(self):
        WorkflowOnlyTasks.__init__(self)
        self.shared['a'] = 'A'
        self._tasks = [self.t_1, self.t_2, self.t_3]

    def t_1(self):
        print('Start')

    def t_2(self):
        print(self.shared['a'])

    def t_3(self):
        print('Finish')


wf = WorkFlow()
wf.run()