from old_f_google.services.big_query.client import BigQuery


bq = BigQuery()

print(f'User = {bq.user}')
print(f'Creds = {bq.creds}')

query = """
            select
                count(*)
            from
                noteret.tiktok.videos_new_by_user_todo
        """
cnt = bq.select.df(query=query)
print(cnt)

