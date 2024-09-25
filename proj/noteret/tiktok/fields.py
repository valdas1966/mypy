from f_google.big_query.structures.field import Field


class Fields:
    """
    ============================================================================
     Class of all Fields in Noteret-Tiktok project.
    ============================================================================
    """

    # Audit
    ID_SESSION = Field.string(name='id_session')
    SOURCE = Field.string(name='source')
    INSERTED = Field.datetime(name='inserted')

    # User Info
    ID_USER = Field.string(name='id_user')
    NICK = Field.string(name='nick')
    REGION = Field.string(name='region')
    IS_VERIFIED = Field.boolean(name='is_verified')
    IS_SECRET = Field.boolean(name='is_secret')
    IS_PRIVATE = Field.boolean(name='is_private')

    # User Stats
    FOLLOWING = Field.integer(name='following')
    FOLLOWERS = Field.integer(name='followers')
    AWEME = Field.integer(name='aweme')
    FAVORITED = Field.integer(name='favorited')
    VIDEOS = Field.integer(name='videos')
    HEARTS = Field.integer(name='hearts')
    DIGGS = Field.integer(name='diggs')

    # Other User
    ID_FOLLOWER = Field.string(name='id_follower')
