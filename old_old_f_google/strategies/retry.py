from google.api_core.retry import Retry as GoogleRetry
from google.api_core.exceptions import GoogleAPICallError,\
                                       TooManyRequests,\
                                       ServiceUnavailable


class Retry(GoogleRetry):
    """
    ============================================================================
     Strategy for Retry commands on Google-Cloud-Platform.
    ============================================================================
    """

    INITIAL: float = 1          # Initial delay in seconds
    MAXIMUM: float = 10         # Maximum delay in seconds
    MULTIPLIER: float = 2       # Multiplier for delay between retries
    DEADLINE: float = 30        # Maximum total time for all retries

    # Exception to Retry (Network Issues)
    EXCEPTIONS = (GoogleAPICallError, TooManyRequests, ServiceUnavailable)

    def __init__(self) -> None:
        GoogleRetry.__init__(self,
                             predicate=Retry.is_retryable_exception,
                             initial=Retry.INITIAL,
                             maximum=Retry.MAXIMUM,
                             multiplier=Retry.MULTIPLIER,
                             deadline=Retry.DEADLINE)

    @staticmethod
    def is_retryable_exception(exception):
        """
        ========================================================================
         Return True if the Exception is Retryable (Network Issues).
        ========================================================================
        """
        return isinstance(exception, Retry.EXCEPTIONS)
