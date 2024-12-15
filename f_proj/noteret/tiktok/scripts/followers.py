from f_google.services.big_query.client import BigQuery
from f_proj.noteret.tiktok.tables import Tables
from f_proj.rapid_api.c_tiktok import TikTok


def run() -> None:
    t = TikTok()
    bq = BigQuery()
    users = bq.select.list(Tables.FOLLOWERS_TODO)
    for id_user in users:
        try:
            cnt = 0
            d_user = t.user.info(id_user=id_user)
            if not d_user:
                print(f'Invalid User {id_user}')
                continue
            _insert_into_users_snapshots(bq=bq, rows=[d_user])
            if d_user['followers'] > 50000:
                print(f'Too much followers ({d_user['followers']}) to {id_user}')
                continue
        except Exception as e:
            print(str(e), id_user)
            continue
        has_more = True
        time = 0
        while has_more:
            try:
                rows, has_more, time = t.user.followers(id_user=id_user, time=time)
                if not rows:
                    break
                keys_followers = {'id_user', 'id_follower'}
                rows_followers = [{k: d[k] for k in keys_followers} for d in rows]
                _insert_into_followers(bq=bq, rows=rows_followers)
                for d in rows:
                    d['id_user'] = d.pop('id_follower')
                _insert_into_users_snapshots(bq=bq, rows=rows)
                cnt += len(rows)
            except Exception as e:
                print(str(e), id_user)
                break
        print(f'{cnt} followers were crawled from {id_user}, '
              f'{d_user['followers']}')


def _insert_into_users_snapshots(bq: BigQuery, rows: list[dict]) -> None:
    tname = Tables.USERS_SNAPSHOTS
    bq.insert.rows_inserted(tname=tname, rows=rows)


def _insert_into_followers(bq: BigQuery, rows: list[dict]) -> None:
    tname = Tables.FOLLOWERS
    bq.insert.rows_inserted(tname=tname, rows=rows)


run()
