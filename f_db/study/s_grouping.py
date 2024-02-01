from f_db.c_sqlite import SQLite
import pandas as pd


col_id = ['a']*7 + ['b']*3
col_n = list(range(10))
col_p = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1]
data = {'id': col_id, 'n': col_n, 'p': col_p}
df = pd.DataFrame(data=data)
sql = SQLite()
sql.load(tname='temp_0', df=df)
query_1 = """
            SELECT 
                id,
                n,
                p,
                CASE WHEN LAG(p) OVER
                                 (PARTITION BY id ORDER BY n) IS DISTINCT
                                  FROM p
                     THEN 1 ELSE 0 END AS change_flag
            FROM 
                temp_0;
        """
sql.ctas(tname='temp_1', query=query_1)
print(sql.select('temp_1'))
sql.close()

