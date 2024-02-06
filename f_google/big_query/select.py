import pandas as pd
from google.cloud import bigquery


class Select:

    def __init__(self, client: bigquery.Client) -> None:
        self._client = client

    def df(self, query: str) -> pd.DataFrame:
        job = self._client.query(query=query)
        return job.to_dataframe()
