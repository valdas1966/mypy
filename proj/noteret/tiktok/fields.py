from f_google.big_query.structures.field import Field


class Fields:
    """
    ============================================================================
     Class of all Fields in Noteret-Tiktok project.
    ============================================================================
    """

    # Audit
    INSERTED = Field.datetime(name='inserted')

    # User
    ID_USER = Field.string(name='id_user')
    NICK = Field.string(name='nick')
    REGION = Field.string(name='region')
    VERIFIED = Field.string(name='verified')
    SECRET = Field.string(name='secret')
    AWEME = Field.integer(name='aweme')
    FAVORITED = Field.integer(name='favorited')
    FOLLOWING = Field.integer(name='following')
    FOLLOWERS = Field.integer(name='followers')

    # Other User
    ID_FOLLOWER = Field.string(name='id_follower')

