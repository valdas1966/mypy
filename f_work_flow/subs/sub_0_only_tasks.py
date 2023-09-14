
class WorkflowOnlyTasks:
    """
    ============================================================================
     Desc: BaseClass for all WorkFlows with List of Tasks.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. run() -> None
           [*] Executes all the Tasks in their specified order.
        2. update_shared(shared: dict) -> None
           [*] Updates the Shared-Attributes Dict.
    ============================================================================
     Attributes:
    ----------------------------------------------------------------------------
        1. tasks: list[callable | WorkFlow]
           [*] List of ordered Tasks to be executed.
        2. shared: dict[str -> any]
           [*] Dict of Shared-Attributes across Tasks.
    ============================================================================
    """

    def __init__(self) -> None:
        # List of ordered Tasks (methods) to be executed
        self._tasks = list()
        # Dict of Shared Attributes across Tasks
        self._shared = dict()

    @property
    def tasks(self) -> list[callable]:
        return self._tasks

    @property
    def shared(self) -> dict[str]:
        return self._shared

    def update_shared(self, shared: dict) -> None:
        """
        ========================================================================
         Desc: Updates the Shared-Attributes Dict.
        ========================================================================
        """
        self._shared.update(shared)

    def run(self) -> None:
        """
        ========================================================================
         Desc: Executes the Tasks in their specified order.
        ========================================================================
        """
        for task in self._tasks:
            self._run_task(task)

    def _run_task(self, task: callable) -> None:
        """
        ========================================================================
         Desc: Executes a given Task.
        ========================================================================
        """
        task()
