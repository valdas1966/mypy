from abc import ABC
from google.cloud.bigquery import Client


class Command(ABC):
    """
    ============================================================================
     Base Class for BigQuery-Commands.
    ============================================================================
    """

    def __init__(self,
                 client: Client,
                 verbose: bool = True) -> None:
        self._client = client
        self._verbose = verbose
