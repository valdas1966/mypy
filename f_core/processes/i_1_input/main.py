from f_core.processes.i_0_abc import ProcessABC
from typing import Any


class ProcessInput(ProcessABC):
    """
    ============================================================================
     ABC for Processes with Input.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 verbose: bool = False,
                 name: str = 'Process Input',
                 **inputs: Any) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
         # Attach inputs as attrs BEFORE base __init__ (so _run can use them)
        self._inputs: dict[str, Any] = inputs
        for key, value in inputs.items():
            setattr(self, key, value)
        ProcessABC.__init__(self, verbose=verbose, name=name)
        