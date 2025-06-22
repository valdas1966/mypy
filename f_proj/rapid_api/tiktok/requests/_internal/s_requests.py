from f_proj.rapid_api.tiktok.requests import RequestsTiktok


def users_by_id() -> None:
    """
    ========================================================================
     Test users_by_id().
    ========================================================================
    """
    id_user = '107955'
    row = RequestsTiktok.users_by_id(id_user=id_user)
    print(row)


def users_by_id_unique() -> None:
    """
    ========================================================================
     Test users_by_id_unique().
    ========================================================================
    """
    id_user_unique = 'tiktok'
    row = RequestsTiktok.users_by_id_unique(id_user_unique=id_user_unique)
    print(row)


def videos_by_user() -> None:
    """
    ========================================================================
     Test videos_by_user().
    ========================================================================
    """
    id_user = '107955'
    rows = RequestsTiktok.videos_by_user(id_user=id_user, limit=10)
    print(rows)


def videos_new_by_user() -> None:
    """
    ========================================================================
     Test videos_new_by_user().
    ========================================================================
    """
    id_user = '107955'
    created = 1750364579
    rows = RequestsTiktok.videos_new_by_user(id_user=id_user, created=created)
    print(rows)


def hashtags_by_keyword() -> None:
    """
    ========================================================================
     Test hashtags_by_keyword().
    ========================================================================
    """
    keyword = 'gaza'
    rows = RequestsTiktok.hashtags_by_keyword(keyword=keyword, limit=10)
    for row in rows:
        print(row)


def videos_by_hashtag() -> None:
    """
    ========================================================================
     Test videos_by_hashtag().
    ========================================================================
    """
    id_hashtag = '1700701060312065'
    rows = RequestsTiktok.videos_by_hashtag(id_hashtag=id_hashtag, limit=10)
    for row in rows:
        print(row)


def followers_by_user() -> None:
    """
    ========================================================================
     Test followers_by_user().
    ========================================================================
    """
    id_user = '107955'
    rows = RequestsTiktok.followers_by_user(id_user=id_user, limit=10)
    for row in rows:
        print(row)


def music_by_id() -> None:
    """
    ========================================================================
     Test music_by_id().
    ========================================================================
    """
    id_music = '7518111689754069773'
    row = RequestsTiktok.music_by_id(id_music=id_music)
    print(row)


def videos_by_music() -> None:
    """
    ========================================================================
     Test videos_by_music().
    ========================================================================
    """
    id_music = '7518111689754069773'
    rows = RequestsTiktok.videos_by_music(id_music=id_music, limit=10)
    for row in rows:
        print(row)


def comments_by_video() -> None:
    """
    ========================================================================
     Test comments_by_video().
    ========================================================================
    """
    id_video = '7518111678504930574'
    rows = RequestsTiktok.comments_by_video(id_video=id_video, limit=10)    
    for row in rows:
        print(row)


users_by_id()
# users_by_id_unique()
# videos_by_user()
# videos_new_by_user()
# hashtags_by_keyword()
# videos_by_hashtag()
# followers_by_user()
# music_by_id()
# videos_by_music()
# comments_by_video()
