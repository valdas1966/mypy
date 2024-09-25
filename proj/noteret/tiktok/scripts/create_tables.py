from f_google.big_query.client import BigQuery
from proj.noteret.tiktok.schemas import Schemas


pre = 'noteret.tiktok'


def users() -> None:
    tname = f'{pre}.users'
    schema = Schemas.users()
    BigQuery().create.table(tname=tname, schema=schema)


def users_snapshots() -> None:
    tname = f'{pre}.users_snapshots'
    schema = Schemas.users_snapshots()
    BigQuery().create.table(tname=tname, schema=schema)


def followers() -> None:
    tname = f'{pre}.followers'
    schema = Schemas.followers()
    BigQuery().create.table(tname=tname, schema=schema)


users()
users_snapshots()
#followers()
