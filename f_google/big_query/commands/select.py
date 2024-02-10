from google.cloud.bigquery.job.query import QueryJob
from f_google.big_query.abc.command import Command
import pandas as pd


class Select(Command):
    """
    ============================================================================
     Class of Select-Commands in BigQuery.
    ============================================================================
    """

    def to_df(self,
              query: str,
              progress_bar_type: str = 'tqdm') -> pd.DataFrame:
        """
        ========================================================================
         Return a Query-Result as a DataFrame.
        ========================================================================
        """
        if ' ' not in query:
            # If it is Table-Name
            query = f'select * from {query}'
        job: QueryJob = self._client.query(query=query)
        return job.to_dataframe(progress_bar_type=progress_bar_type)
