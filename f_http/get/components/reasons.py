from enum import Enum, auto


class Reasons(Enum):
    """
    ============================================================================
     Enum for Http Get-Request fails Reasons.
    ============================================================================
    """
    COMMUNICATION = auto()  # Issues with network connectivity
    TIMEOUT = auto()  # Request timed out
    FORBIDDEN = auto()  # HTTP 403 Forbidden
    UNAUTHORIZED = auto()  # HTTP 401 Unauthorized
    NOT_FOUND = auto()  # HTTP 404 Not Found
    SERVER_ERROR = auto()  # HTTP 500 Internal Server Error
    BAD_REQUEST = auto()  # HTTP 400 Bad Request
    RATE_LIMIT = auto()  # HTTP 429 Too Many Requests
    UNKNOWN = auto()  # Catch-all for any other unknown error
