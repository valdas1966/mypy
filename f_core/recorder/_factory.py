from f_core.recorder.main import Recorder


class Factory:
    """
    ========================================================================
     Factory for the Recorder class.
    ========================================================================
    """

    @staticmethod
    def active() -> Recorder:
        """
        ====================================================================
         Create an active Recorder.
        ====================================================================
        """
        return Recorder(is_active=True)

    @staticmethod
    def inactive() -> Recorder:
        """
        ====================================================================
         Create an inactive Recorder.
        ====================================================================
        """
        return Recorder(is_active=False)
