from f_google.services.big_query.structures.field import Field


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
    IS_BROKEN = Field.boolean(name='is_broken')
    IS_OK = Field.boolean(name='is_ok')
    INSERTED = Field.datetime(name='inserted')

    # User Info
    ID_USER = Field.string(name='id_user')
    ID_USER_UNIQUE = Field.string(name='id_user_unique')
    NICK = Field.string(name='nick')
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

    # Music
    ID_MUSIC = Field.string(name='id_music')

    # Hashtag
    ID_HASHTAG = Field.string(name='id_hashtag')

    # Comment
    ID_COMMENT = Field.string(name='id_comment')
    TEXT = Field.string(name='text')
    REPLIES = Field.integer(name='replies')

    # Video
    ID_VIDEO = Field.string(name='id_video')
    REGION = Field.string(name='region')
    TITLE = Field.string(name='title')
    CREATED = Field.integer(name='created')
    DURATION = Field.integer(name='duration')
    PLAYS = Field.integer(name='plays')
    SHARES = Field.integer(name='shares')
    DIGGS = Field.integer(name='diggs')
    DOWNLOADS = Field.integer(name='downloads')
    COMMENTS = Field.integer(name='comments')
    IS_AD = Field.boolean(name='is_ad')

    @staticmethod
    def user_info() -> list[Field]:
        fields: list[Field] = list()
        fields.append(Fields.ID_USER)
        fields.append(Fields.ID_USER_UNIQUE)
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

    @staticmethod
    def audit_post() -> list[Field]:
        """
        ========================================================================
         Return a list of Audit-Fields in the end of the table.
        ========================================================================
        """
        fields: list[Field] = list()
        fields.append(Fields.IS_FOUND)
        fields.append(Fields.IS_BROKEN)
        fields.append(Fields.IS_OK)
        fields.append(Fields.INSERTED)
        return fields
