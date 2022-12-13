from f_abstract.validdable import Validdable


class Runnable(Validdable):
    """
    ============================================================================
     Description: Class with Secured (Try-Except) Runnable function
                  (enriched with Pre-Run, Post-Run, and On-Error functions).
    ============================================================================
    """

    def __init__(self, **kwargs):
        Validdable.__init__(self, **kwargs)
        self._pre_run()
        try:
            self._run()
            self._is_valid = True
        except Exception as e:
            self._is_valid = False
            self._e_msg = str(e)
            self._on_error()
            # raise Exception(self._e_msg)
        self._post_run()

    def _run(self) -> None:
        """
        ========================================================================
         Description: Run Commands.
        ========================================================================
        """
        pass

    def _pre_run(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Run Pre-Run Commands.
        ========================================================================
        """
        pass

    def _post_run(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Run Post-Run Commands.
        ========================================================================
        """
        pass

    def _on_error(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Run On-Error Scenario.
        ========================================================================
        """
        pass
