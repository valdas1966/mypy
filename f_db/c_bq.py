from google.cloud import bigquery
import pandas as pd
import os


class BigQuery:

    def __init__(self, json_key: str):
        """
        ========================================================================
         Description: Constructor - Initialize the Connection.
        ========================================================================
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_key
        self._client = bigquery.Client()

    def select(self,
               query: str,  # SQL-Query or Table-Name
               limit: int = -1
               ) -> pd.DataFrame:
        """
        ========================================================================
         Description: Load Query Results into DataFrame.
        ========================================================================
        """
        if ' ' not in query:
            tname = query
            query = f'select * from {tname}'
        if limit > -1:
            query += f' limit {limit}'
        df = self._client.query(query).result().to_dataframe()
        return df

    def select_list(self,
                    query: str,  # SQL-Query or Table-Name
                    col: str = None) -> 'list[str]':
        """
        ========================================================================
         Description: Return Specified Column as a List of str.
                        If a Column-Name is not given - Return First Column.
        ========================================================================
        """
        df = self.select(query=query)
        if col:
            li = df[col].to_list()
        else:
            li = df.iloc[:, 0].to_list()
        return [str(x) for x in li]

    def select_value(self, query: str) -> any:
        """
        ========================================================================
         Description: Return the First-Value (from the first Row and Col).
        ========================================================================
        """
        df = self.select(query=query)
        return df.iloc[0][0]

    def run(self, command: str) -> None:
        """
        ========================================================================
         Description: Run a BigQuery-Command.
        ========================================================================
        """
        job = self._client.query(command)
        job.result()

    def create(self,
               tname: str,
               cols: 'list[str]') -> None:
        """
        ========================================================================
         Description: Create Table by given TName and Cols Signature.
        ========================================================================
        """
        self.drop(tname, report=False)
        str_cols = ','.join(cols)
        self.run(f'create table {tname}({str_cols})')

    def ctas(self,
             tname: str,
             query: str) -> None:
        """
        ========================================================================
         Description: Create Table (tname) as Query.
        ========================================================================
        """
        job_config = bigquery.QueryJobConfig(destination=tname)
        self.drop(tname, report=False)
        job = self._client.query(query=query, job_config=job_config)
        job.result()

    def count(self, tname: str) -> int:
        """
        ========================================================================
         Description: Return Number of Rows in the Table.
        ========================================================================
        """
        df = self.select(f'select count(*) from {tname}')
        cnt = int(df.iloc(0)[0][0])
        return cnt

    def count_duplicate_rows(self,
                             tname: str,
                             limit: int) -> pd.DataFrame:
        cols = self.cols(tname=tname)
        cols = ', '.join(cols)
        query = f"""
                    select
                        {cols},
                        count(*) as cnt
                    from
                        {tname}
                    group by
                        {cols}
                    order by
                        count(*) desc
                """
        return self.select(query=query, limit=limit)

    def is_exists(self, tname: str) -> bool:
        """
        ========================================================================
         Description: Return True if there exists table with the given name.
        ========================================================================
        """
        try:
            self.count(tname)
            return True
        except Exception:
            return False

    def insert_rows(self,
                    tname: str,
                    rows: 'list of dict') -> None:
        """
        ========================================================================
         Description: Get BigQuery Table-Name and List of Rows (Dicts). Insert
                       the Rows into the BigQuery Table.
        ========================================================================
        """
        table = self._client.get_table(tname)
        ans = self._client.insert_rows(table=table,
                                       rows=rows,
                                       #ignore_unknown_values=True,
                                       skip_invalid_rows=True)
        if ans:
            raise Exception(f"{ans[0]['errors'][0]['message']}\n{rows}")

    def insert_into(self,
                    tname_from: str,
                    tname_to: str,
                    cols: list = None) -> None:
        """
        ========================================================================
         Description: Insert rows from one BigQuery table into another.
        ========================================================================
        """
        if cols:
            str_cols = ','.join(cols)
            command = f"""insert into {tname_to}({str_cols})
                          select {str_cols} from {tname_from}
                        """
        else:
            command = f'insert into {tname_to} select * from {tname_from}'
        self.run(command)

    def insert_if_not_exist(self,
                            tname_a: str,
                            tname_b: str) -> None:
        """
        ========================================================================
            Desc: Insert into B rows from A that are not exist in B.
        ========================================================================
        """
        cols = self.cols(tname=tname_b)
        cols_t1 = ', '.join([f't1.{col}' for col in cols])
        cols_equals = ' and '.join([f"COALESCE(CAST(t1.{col} as string), '')="
                                    f"COALESCE(CAST(t2.{col} as string), '')"
                                    for col in cols])
        cols_is_null = ' and '.join([f't2.{col} is null' for col in cols])
        command = f"""
                        insert into {tname_b}
                        select {cols_t1}
                        from {tname_a} t1
                        left join {tname_b} t2
                        on {cols_equals}
                        where {cols_is_null}
                    """
        self.run(command=command)

    def load(self,
             df: pd.DataFrame,
             tname: str,
             append: bool = False) -> None:
        """
        ========================================================================
         Description: Load DataFrame into BigQuery Table.
        ========================================================================
        """
        if_exists = 'append' if append else 'replace'
        self.drop(tname, report=False)
        # self._client.load_table_from_dataframe(df, destination=tname)
        df.to_gbq(destination_table=tname, if_exists=if_exists)

    def insert_into_from_json(self,
                              str_json: str,
                              tname: str):
        self._client.load_table_from_json(json_rows=str_json,
                                          destination=tname)

    def insert_rows_json(self,
                         rows: list,
                         tname: str):
        job = self._client.insert_rows_json(tname, rows,
                                            ignore_unknown_values=True)
                                            # ,skip_invalid_rows=True)
        if job:
            raise Exception(str(job))

    def drop(self, tname: str, report: bool = False) -> None:
        """
        ========================================================================
         Description: Drop Table (if exists).
        ========================================================================
        """
        command = f'drop table {tname}'
        try:
            self.run(command=command)
        except Exception as e:
            if report:
                raise Exception(e)

    def cols(self, tname: str) -> list:
        """
        ========================================================================
         Desc: Return Table Column-Names as list[str].
        ========================================================================
        """
        table = self._client.get_table(tname)
        return [field.name for field in table.schema]

    def close(self):
        """
        ========================================================================
         Description: Close the BigQuery connection.
        ========================================================================
        """
        self._client.close()

    def __repr__(self):
        return "'Class BigQuery'"
