from f_google.services.big_query.structures.schema import Schema
from f_proj.noteret.tiktok.fields import Fields


class Schemas:
    """
    ============================================================================
     Class of Schemas for Noteret-Tiktok project.
    ============================================================================
    """

    _PRE = 'noteret.tiktok'

    @staticmethod
    def users() -> Schema:
        tname = 'users'
        schema = Schemas._create_schema(tname=tname)
        schema.extend(Fields.user_info())
        schema.extend(Fields.user_stats())
        schema.append(Fields.INSERTED)
        return schema

    @staticmethod
    def users_snapshots() -> Schema:
        tname = 'users_snapshots'
        schema = Schemas._create_schema(tname=tname)
        schema.extend(Fields.user_info())
        schema.extend(Fields.user_stats())
        schema.append(Fields.SOURCE)
        schema.append(Fields.IS_FOUND)
        schema.append(Fields.IS_OK)
        schema.append(Fields.INSERTED)
        return schema

    @staticmethod
    def followers() -> Schema:
        tname = 'followers'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        schema.append(Fields.ID_FOLLOWER)
        schema.append(Fields.INSERTED)
        return schema

    @staticmethod
    def followers_todo() -> Schema:
        tname = 'followers_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        return schema

    @staticmethod
    def following_todo() -> Schema:
        tname = 'following_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        return schema

    @staticmethod
    def users_snapshots_todo() -> Schema:
        tname = 'users_snapshots_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        return schema

    @staticmethod
    def videos_by_music() -> Schema:
        tname = 'videos_by_music'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_MUSIC)
        schema.append(Fields.ID_USER)
        schema.append(Fields.ID_VIDEO)
        schema.append(Fields.IS_OK)
        schema.append(Fields.IS_FOUND)
        schema.append(Fields.INSERTED)
        return schema
    
    @staticmethod
    def videos_by_hashtag() -> Schema:
        tname = 'videos_by_hashtag'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_HASHTAG)
        schema.append(Fields.ID_USER)
        schema.append(Fields.ID_USER_UNIQUE)
        schema.append(Fields.NICK)
        schema.append(Fields.REGION)
        schema.append(Fields.ID_VIDEO)
        schema.append(Fields.TITLE)
        schema.append(Fields.CREATED)
        schema.append(Fields.DURATION)
        schema.append(Fields.PLAYS)
        schema.append(Fields.SHARES)
        schema.append(Fields.DIGGS)
        schema.append(Fields.DOWNLOADS)
        schema.append(Fields.COMMENTS)
        schema.append(Fields.IS_AD)
        schema.append(Fields.IS_OK)
        schema.append(Fields.IS_FOUND)
        schema.append(Fields.INSERTED)
        return schema

    @staticmethod
    def videos_by_hashtag_todo() -> Schema:
        tname = 'videos_by_hashtag_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_HASHTAG)
        return schema
    
    @staticmethod
    def comments_by_video() -> Schema:
        tname = 'comments_by_video'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_COMMENT)
        schema.append(Fields.TEXT)
        schema.append(Fields.ID_VIDEO)
        schema.append(Fields.DIGGS)
        schema.append(Fields.REPLIES)
        schema.append(Fields.CREATED)
        schema.append(Fields.ID_USER)
        schema.append(Fields.ID_USER_UNIQUE)
        schema.append(Fields.NICK)
        schema.append(Fields.REGION)
        schema.append(Fields.AWEME)
        schema.append(Fields.FAVORITED)
        schema.append(Fields.FOLLOWERS) 
        schema.append(Fields.FOLLOWING)
        schema.append(Fields.IS_OK)
        schema.append(Fields.IS_FOUND)
        schema.append(Fields.INSERTED)
        return schema
    
    @staticmethod
    def comments_by_video_todo() -> Schema:
        tname = 'comments_by_video_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_VIDEO)
        return schema
    
    @staticmethod
    def _create_schema(tname: str) -> Schema:
        name = Schemas._to_name(tname=tname)
        return Schema(name=name)

    @staticmethod
    def _to_name(tname: str) -> str:
        return f'{Schemas._PRE}_{tname}'
