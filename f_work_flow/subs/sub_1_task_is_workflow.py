from __future__ import annotations
from f_work_flow.subs.sub_0_only_tasks import WorkflowOnlyTasks


class WorkFlowTaskIsWorkFlow(WorkflowOnlyTasks):
    """
    ============================================================================
     Desc: WorkFlow class that can include another WorkFlow as one of its Tasks.
    ============================================================================
    """

    def __init__(self, shared: dict = dict()) -> None:
        """
        ========================================================================
         Desc: Inits the WorkFlow with an optional Shared-Attributes Dict.
        ========================================================================
        """
        WorkflowOnlyTasks.__init__(self)
        self._shared.update(shared)

    def _run_task(self, task: callable | WorkFlowTaskIsWorkFlow) -> None:
        """
        ========================================================================
         Desc: Executes the Task. The Task can be Callable or WorkFlow.
                If it is a Workflow, executes all its tasks and update the
                 shared-attributes dict.
        ========================================================================
        """
        if callable(task):
            WorkflowOnlyTasks._run_task(task)
        elif task is WorkFlowTaskIsWorkFlow:
            wf = task(shared=self.shared)
            wf.run()
            self._shared.update(wf.shared)
