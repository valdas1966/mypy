from old_old_f_google.services.big_query.client import BigQuery


def insert_select() -> None:
    """
    ========================================================================
     Insert into BigQuery using a SELECT query.
    ========================================================================
    """
    bq = BigQuery()
    query = """
                select
                    id_user,
                    max(created) as created
                from
                    noteret.tiktok.videos_by_user
                where
                    created is not null
                group by
                    id_user
            """
    bq.insert.select(name_table='noteret.tiktok.videos_new_by_user_todo',
                     query=query)


insert_select()
