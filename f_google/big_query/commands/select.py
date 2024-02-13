from google.cloud.bigquery.job.query import QueryJob
from f_google.big_query.abc.command import Command
from f_google.strategies.retry import Retry
import pandas as pd


class Select(Command):
    """
    ============================================================================
     Class of Select-Commands in BigQuery.
    ============================================================================
    """

    def to_df(self, query: str) -> pd.DataFrame:
        """
        ========================================================================
         Return a Query-Result as a DataFrame.
        ========================================================================
        """
        if ' ' not in query:
            # If it is Table-Name
            query = f'select * from {query}'
        job: QueryJob = self._client.query(query=query, retry=Retry())
        if self._verbose:
            df = job.to_dataframe(progress_bar_type='tqdm')
            print(f'Selected [{len(df)}] rows.')
        else:
            df = job.to_dataframe()
        return df
