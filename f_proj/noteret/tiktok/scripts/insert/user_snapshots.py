from f_google.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.api import TiktokAPI
from f_proj.noteret.tiktok.tables import Tables
from f_utils import u_datetime


def prod():
    bq = BigQuery()
    users = bq.select.list(Tables.USERS_SNAPSHOTS_TODO)
    for i, id_user in enumerate(users):
        tname = Tables.USERS_SNAPSHOTS
        d = TiktokAPI.user_snapshot(id_user).to_dict()
        bq.insert.rows_inserted(tname=tname, rows=[d])
        print(u_datetime.now(), f'[{i+1} / {len(users)}]')


def t():
    bq = BigQuery()
    users = ['107955', '12345']
    for id_user in users:
        tname = Tables.USERS_SNAPSHOTS
        data = TiktokAPI.user_snapshot(id_user=id_user)
        bq.insert.rows_inserted(tname=tname, rows=[data.to_dict()])


# t()
prod()
