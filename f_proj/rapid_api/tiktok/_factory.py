class Factory:
    """
    ============================================================================
     Factory for ApiTikTok Integration Test Data.
    ============================================================================
     Uses the official @tiktok account as stable test subject.
     Volatile IDs (video, music) are fetched live from the API.
    ============================================================================
    """

    # Stable: official TikTok account (verified, public)
    ID_USER = '107955'
    ID_USER_UNIQUE = 'tiktok'
    # Stable: #tiktok hashtag
    ID_HASHTAG = '23428'
    # Stable: search keyword
    KEYWORD = 'tiktok'

    # =================================================================
    #  Type Schemas (field_name -> expected_type)
    # =================================================================

    SCHEMA_USER_BY_ID = {
        'id_user': str,
        'id_user_unique': str,
        'nick': str,
        'is_verified': bool,
        'is_secret': bool,
        'is_private': bool,
        'videos': int,
        'hearts': int,
        'diggs': int,
        'followers': int,
        'following': int,
        'signature': str,
        'twitter': str,
        'youtube': str,
        'avatar': str,
        'is_ok': bool,
        'is_broken': bool,
    }

    SCHEMA_USER_BY_ID_UNIQUE = {
        'id_user': str,
        'id_user_unique': str,
        'nick': str,
        'is_verified': bool,
        'is_secret': bool,
        'is_private': bool,
        'videos': int,
        'hearts': int,
        'diggs': int,
        'followers': int,
        'following': int,
        'is_found': bool,
        'is_ok': bool,
        'is_broken': bool,
    }

    SCHEMA_VIDEO = {
        'id_user': str,
        'id_music': str,
        'id_video': str,
        'region': str,
        'title': str,
        'created': int,
        'duration': int,
        'plays': int,
        'shares': int,
        'diggs': int,
        'comments': int,
        'downloads': int,
        'is_ad': bool,
        'play': str,
        'is_found': bool,
        'is_ok': bool,
        'is_broken': bool,
    }

    SCHEMA_HASHTAG = {
        'keyword': str,
        'id_hashtag': str,
        'hashtag': str,
        'users': int,
        'views': int,
        'is_ok': bool,
        'is_broken': bool,
    }

    SCHEMA_VIDEO_BY_HASHTAG = {
        'id_hashtag': str,
        'id_user': str,
        'id_user_unique': str,
        'nick': str,
        'id_video': str,
        'region': str,
        'title': str,
        'created': int,
        'duration': int,
        'plays': int,
        'shares': int,
        'diggs': int,
        'comments': int,
        'downloads': int,
        'is_ad': bool,
        'play': str,
        'is_ok': bool,
        'is_broken': bool,
    }

    SCHEMA_FOLLOWER = {
        'id_user': str,
        'id_follower': str,
        'id_user_unique': str,
        'nick': str,
        'region': str,
        'is_verified': bool,
        'is_secret': bool,
        'followers': int,
        'following': int,
        'aweme': int,
        'favorited': int,
        'is_ok': bool,
        'is_broken': bool,
    }

    SCHEMA_MUSIC = {
        'id_music': str,
        'title': str,
        'play': str,
        'author': str,
        'duration': int,
        'is_original': bool,
        'videos': int,
        'is_ok': bool,
        'is_broken': bool,
    }

    SCHEMA_VIDEO_BY_MUSIC = {
        'id_music': str,
        'id_video': str,
        'id_user': str,
        'is_ok': bool,
        'is_broken': bool,
    }

    SCHEMA_COMMENT = {
        'id_video': str,
        'id_comment': str,
        'text': str,
        'replies': int,
        'diggs': int,
        'created': int,
        'id_user': str,
        'id_user_unique': str,
        'nick': str,
        'region': str,
        'aweme': int,
        'favorited': int,
        'followers': int,
        'following': int,
        'is_ok': bool,
        'is_broken': bool,
    }
