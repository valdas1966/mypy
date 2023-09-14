from __future__ import annotations


class Workflow:
    """
    ============================================================================
     Desc: BaseClass for all WorkFlows.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. run() -> None
           [*] Executes all the Tasks in their specified order.
    ============================================================================
     Protected Attributes:
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

    def run(self) -> None:
        """
        ========================================================================
         Desc: Executes the Tasks in their specified order.
        ========================================================================
        """
        for task in self._tasks:
            task()

    def _run_task(self, task: callable | Workflow) -> None:
        if callable(task):
            task()
        elif isinstance(task, Workflow):
            
