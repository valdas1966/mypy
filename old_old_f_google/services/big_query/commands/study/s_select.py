from old_old_f_google.services.big_query.client import BigQuery


query = """
            select
                *
            from
                noteret.tiktok2.test_insert_1
            order by
                inserted desc
        """
bq = BigQuery(user='RAMI')
df = bq.select.to_df(query=query)

print(df)

