from old_old_f_google.services.big_query.client import BigQuery


def videos_new_by_user_todo() -> None:
    bq = BigQuery()
    bq.truncate.table(name_table='noteret.tiktok.videos_new_by_user_todo')


videos_new_by_user_todo()