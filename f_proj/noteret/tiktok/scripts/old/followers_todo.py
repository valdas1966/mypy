from old_old_f_google.services.big_query.client import BigQuery


query = """
            insert into
                noteret.tiktok.followers_todo(id_user)
            select
                distinct id_user
            from
                noteret.tiktok.users_snapshots
            limit 100
        """

bq = BigQuery()
bq._client.query(query=query)
