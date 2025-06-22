from google.cloud.bigquery.job.query import QueryJob
from old_f_google.services.big_query.abc.command import Command
from old_f_google.strategies.retry import Retry
import pandas as pd


class Select(Command):
    """
    ============================================================================
     Class of Select-Commands in BigQuery.
    ============================================================================
    """

    def df(self, query: str) -> pd.DataFrame:
        """
        ========================================================================
         Return list Query-Result as list DataFrame.
        ========================================================================
        """
        if ' ' not in query:
            # If it is Table-Name
            query = f'select * from {query}'
        job: QueryJob = self._client.query(query=query, retry=Retry())
        if self._verbose:
            _df = job.to_dataframe(progress_bar_type='tqdm')
            print(f'Selected [{len(_df)}] rows.')
        else:
            _df = job.to_dataframe()
        return _df

    def list(self, query: str) -> list:
        """
        ========================================================================
         Return the First-Col of the Query-Result as list of Values.
        ========================================================================
        """
        df = self.df(query=query)
        if df.empty:
            return list()
        return df.iloc[:, 0].tolist()
