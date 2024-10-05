from abc import ABC
from f_abstract.components.rate_success import RateSuccess


class QuestionBase(ABC):
    """
    ============================================================================
     Abstract-Class that manages basic statistics related to list questions.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # _stats.total = Number of times the Question was asked.
        # _stats.success = Number of times the Question was answered correctly.
        self._stats = RateSuccess()

    @property
    # Stats about the Question's History
    def stats(self) -> RateSuccess:
        return self._stats
