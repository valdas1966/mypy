from old_f_google.services.big_query.client import BigQuery
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


def followers_by_user() -> None:
    """
    ========================================================================
     Create table 'Followers_by_User'.
    ========================================================================
    """
    tname = Tables.FOLLOWERS_BY_USER
    schema = Schemas.followers_by_user()
    BigQuery().create.table(tname=tname, schema=schema)


def followers_by_user_todo() -> None:
    """
    ========================================================================
     Create table 'Followers_by_User_Todo'.
    ========================================================================
    """
    tname = Tables.FOLLOWERS_BY_USER_TODO
    schema = Schemas.followers_by_user_todo()
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


def users_by_id_unique_todo() -> None:
    """
    ========================================================================
     Create table 'Users_by_Id_Unique_Todo'.
    ========================================================================
    """
    tname = Tables.USERS_BY_ID_UNIQUE_TODO
    schema = Schemas.users_by_id_unique_todo()
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


def videos_new_by_user() -> None:
    """
    ========================================================================
     Create table 'Videos_New_by_User'.
    ========================================================================
    """
    tname = Tables.VIDEOS_NEW_BY_USER
    schema = Schemas.videos_new_by_user()
    BigQuery().create.table(tname=tname, schema=schema)


def videos_new_by_user_todo() -> None:
    """
    ========================================================================
     Create table 'Videos_New_by_User_Todo'.
    ========================================================================
    """
    tname = Tables.VIDEOS_NEW_BY_USER_TODO
    schema = Schemas.videos_new_by_user_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def hashtags_by_keyword() -> None:
    """
    ========================================================================
     Create table 'Hashtags_by_Keyword'.
    ========================================================================
    """ 
    tname = Tables.HASHTAGS_BY_KEYWORD
    schema = Schemas.hashtags_by_keyword()
    BigQuery().create.table(tname=tname, schema=schema)


def hashtags_by_keyword_todo() -> None:
    """
    ========================================================================
     Create table 'Hashtags_by_Keyword_Todo'.
    ========================================================================
    """ 
    tname = Tables.HASHTAGS_BY_KEYWORD_TODO
    schema = Schemas.hashtags_by_keyword_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def videos_by_hashtag_todo() -> None:
    """
    ========================================================================
     Create table 'Videos_by_Hashtag_Todo'.
    ========================================================================
    """
    tname = Tables.VIDEOS_BY_HASHTAG_TODO
    schema = Schemas.videos_by_hashtag_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def videos_by_hashtag() -> None:
    """
    ========================================================================
     Create table 'Videos_by_Hashtag'.
    ========================================================================
    """
    tname = Tables.VIDEOS_BY_HASHTAG
    schema = Schemas.videos_by_hashtag()
    BigQuery().create.table(tname=tname, schema=schema)


def music_by_id() -> None:
    """
    ========================================================================
     Create table 'Music_by_Id'.
    ========================================================================
    """
    tname = Tables.MUSIC_BY_ID
    schema = Schemas.music_by_id()
    BigQuery().create.table(tname=tname, schema=schema) 


def music_by_id_todo() -> None:
    """
    ========================================================================
     Create table 'Music_by_Id_Todo'.
    ========================================================================
    """ 
    tname = Tables.MUSIC_BY_ID_TODO
    schema = Schemas.music_by_id_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def download_todo() -> None:
    """
    ========================================================================
     Create table 'Download_Todo'.
    ========================================================================
    """ 
    tname = Tables.DOWNLOAD_TODO
    schema = Schemas.download_todo()
    BigQuery().create.table(tname=tname, schema=schema)


def download_done() -> None:
    """
    ========================================================================
     Create table 'Download_Done'.
    ========================================================================
    """ 
    tname = Tables.DOWNLOAD_DONE    
    schema = Schemas.download_done()
    BigQuery().create.table(tname=tname, schema=schema)


# users()
# users_snapshots()
# followers()
# followers_todo()
# users_valid_todo()
# videos_by_music()
# videos_by_hashtag()
# videos_by_hashtag_todo()
# comments_by_video()
# comments_by_video_todo()
# users_by_id()
# users_by_id_todo()
# videos_by_user()
# videos_by_user_todo()
# videos_new_by_user()
# videos_new_by_user_todo()
# users_by_id_unique_todo()
# hashtags_by_keyword()
# hashtags_by_keyword_todo()
# videos_by_hashtag()
# videos_by_hashtag_todo()
# followers_by_user()
# followers_by_user_todo()
# music_by_id()
# music_by_id_todo()
# download_todo()
download_done()
