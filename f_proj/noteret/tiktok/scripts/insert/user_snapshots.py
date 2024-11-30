from f_google.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.api import TiktokAPI
from f_proj.noteret.tiktok.tables import Tables


bq = BigQuery()
users = bq.select.list(Tables.USERS_SNAPSHOTS_TODO)
for id_user in users:
    tname = Tables.USERS_SNAPSHOTS
    d = TiktokAPI.user_snapshot(id_user).to_dict()
    bq.insert.rows_inserted(tname=tname, rows=[d])
