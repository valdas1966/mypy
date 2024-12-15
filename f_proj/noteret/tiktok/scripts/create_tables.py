from f_google.services.big_query.client import BigQuery
from f_proj.noteret.tiktok.schemas import Schemas
from f_proj.noteret.tiktok.tables import Tables


pre = 'noteret.tiktok'


def users() -> None:
    tname = Tables.USERS
    schema = Schemas.users()
    BigQuery().create.table(tname=tname, schema=schema)


def users_snapshots() -> None:
    tname = Tables.USERS_SNAPSHOTS
    schema = Schemas.users_snapshots()
    BigQuery().create.table(tname=tname, schema=schema)


def followers() -> None:
    tname = Tables.FOLLOWERS
    schema = Schemas.followers()
    BigQuery().create.table(tname=tname, schema=schema)


def followers_todo() -> None:
    tname = Tables.FOLLOWERS_TODO
    schema = Schemas.followers_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def following_todo() -> None:
    tname = Tables.FOLLOWING_TODO
    schema = Schemas.following_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def users_valid_todo() -> None:
    tname = Tables.USERS_VALID_TODO
    schema = Schemas.users_valid_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def videos_by_music() -> None:
    tname = Tables.VIDEOS_BY_MUSIC
    schema = Schemas.videos_by_music()
    BigQuery().create.table(tname=tname, schema=schema)


# users()
# users_snapshots()
# followers()
# followers_todo()
# following_todo()
# users_valid_todo()
videos_by_music()
