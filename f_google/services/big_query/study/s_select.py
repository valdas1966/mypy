from f_google.services.big_query.client import BigQuery


def created() -> None:
    bq = BigQuery()
    query = """
                select
                    id_user,
                    created
                from
                    noteret.tiktok.videos_new_by_user_todo
                where
                    id_user = '6897562973927228417'
            """
    df = bq.select.df(query=query)
    print(df)
    

def videos_new_by_user_todo() -> None:
    bq = BigQuery()
    query = """
                select
                    *
                from
                    noteret.tiktok.videos_new_by_user_todo
                limit 10
            """
    df = bq.select.df(query=query)
    print(df)


videos_new_by_user_todo()
# created()
