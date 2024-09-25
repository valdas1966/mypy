from f_google.big_query.client import BigQuery
from proj.rapid_api.c_tiktok import TikTok


tname_users_snapshots = 'noteret.tiktok.users_snapshots'
tname_followers = 'noteret.tiktok.followers'


def run(id_user: str) -> None:
    t = TikTok()
    bq = BigQuery()
    d_user = t.user.info(id_user=id_user)
    if not d_user:
        print(f'Invalid User {id_user}')
        return None
    bq.insert.rows_inserted(tname=tname_users_snapshots, rows=[d_user])
    has_more = True
    time = 0
    while has_more:
        rows, has_more, time = t.user.followers(id_user=id_user, time=time)
        keys_followers = {'id_user', 'id_follower'}
        rows_followers = [{k: d[k] for k in keys_followers} for d in rows]
        bq.insert.rows_inserted(tname=tname_followers, rows=rows_followers)
        for d in rows:
            d['id_user'] = d.pop('id_follower')
        bq.insert.rows_inserted(tname=tname_users_snapshots, rows=rows)


run(id_user='129067350212964352')
