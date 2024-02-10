from google.cloud.bigquery import Client


class Insert:

    def __init__(self, client: Client) -> None:
        self._client = client
