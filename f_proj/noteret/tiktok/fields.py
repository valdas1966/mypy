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
    IS_FOUND = Field.boolean(name='is_found')
    IS_OK = Field.boolean(name='is_ok')
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

    @staticmethod
    def user_info() -> list[Field]:
        fields: list[Field] = list()
        fields.append(Fields.ID_USER)
        fields.append(Fields.NICK)
        fields.append(Fields.REGION)
        fields.append(Fields.IS_VERIFIED)
        fields.append(Fields.IS_SECRET)
        fields.append(Fields.IS_PRIVATE)
        return fields

    @staticmethod
    def user_stats() -> list[Field]:
        fields: list[Field] = list()
        fields.append(Fields.FOLLOWING)
        fields.append(Fields.FOLLOWERS)
        fields.append(Fields.AWEME)
        fields.append(Fields.FAVORITED)
        fields.append(Fields.VIDEOS)
        fields.append(Fields.HEARTS)
        fields.append(Fields.DIGGS)
        return fields
