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


def videos_by_hashtag() -> None:
    tname = Tables.VIDEOS_BY_HASHTAG
    schema = Schemas.videos_by_hashtag()
    BigQuery().create.table(tname=tname, schema=schema)


def videos_by_hashtag_todo() -> None:
    tname = Tables.VIDEOS_BY_HASHTAG_TODO
    schema = Schemas.videos_by_hashtag_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def comments_by_video() -> None:
    tname = Tables.COMMENTS_BY_VIDEO
    schema = Schemas.comments_by_video()
    BigQuery().create.table(tname=tname, schema=schema)


def comments_by_video_todo() -> None:
    tname = Tables.COMMENTS_BY_VIDEO_TODO
    schema = Schemas.comments_by_video_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def users_by_id() -> None:
    """
    ========================================================================
     Create table 'Users_by_Id'.
    ========================================================================
    """
    tname = Tables.USERS_BY_ID
    schema = Schemas.users_by_id()
    BigQuery().create.table(tname=tname, schema=schema)


def users_by_id_todo() -> None:
    """
    ========================================================================
     Create table 'Users_by_Id_Todo'.
    ========================================================================
    """
    tname = Tables.USERS_BY_ID_TODO
    schema = Schemas.users_by_id_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def videos_by_user() -> None:
    """
    ========================================================================
     Create table 'Videos_by_User'.
    ========================================================================
    """
    tname = Tables.VIDEOS_BY_USER
    schema = Schemas.videos_by_user()
    BigQuery().create.table(tname=tname, schema=schema)


def videos_by_user_todo() -> None:
    """
    ========================================================================
     Create table 'Videos_by_User_Todo'.
    ========================================================================
    """
    tname = Tables.VIDEOS_BY_USER_TODO
    schema = Schemas.videos_by_user_todo()
    BigQuery().create.table(tname=tname, schema=schema)


# users()
# users_snapshots()
# followers()
# followers_todo()
# following_todo()
# users_valid_todo()
# videos_by_music()
# videos_by_hashtag()
# videos_by_hashtag_todo()
# comments_by_video()
# comments_by_video_todo()
users_by_id()
users_by_id_todo()
# videos_by_user()
# videos_by_user_todo()
