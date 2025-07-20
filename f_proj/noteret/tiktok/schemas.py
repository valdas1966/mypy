from old_f_google.services.big_query.structures.schema import Schema
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
    def followers() -> Schema:
        tname = 'followers'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        schema.append(Fields.ID_FOLLOWER)
        schema.append(Fields.INSERTED)
        return schema

    @staticmethod
    def followers_by_user() -> Schema:
        """
        ========================================================================
         Return schema for table 'Followers_by_User'.
        ========================================================================
        """
        tname = 'followers_by_user'
        schema = Schemas._create_schema(tname=tname)
        schema.extend(Fields.user_info())
        schema.extend(Fields.user_stats())
        schema.append(Fields.ID_FOLLOWER)
        schema.append(Fields.REGION)
        schema.extend(Fields.audit())
        return schema
    
    @staticmethod   
    def followers_by_user_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Followers_by_User_Todo'.
        ========================================================================
        """
        tname = 'followers_by_user_todo'
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
        return schema
    
    @staticmethod
    def comments_by_video_todo() -> Schema:
        tname = 'comments_by_video_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_VIDEO)
        return schema

    @staticmethod
    def users_by_id() -> Schema:
        """
        ========================================================================
         Return schema for table 'Users_by_Id'.
        ========================================================================
        """
        tname = 'users_by_id'
        schema = Schemas._create_schema(tname=tname)
        schema.extend(Fields.user_info())
        schema.extend(Fields.user_stats())
        schema.extend(Fields.audit_post())
        return schema
    
    @staticmethod
    def users_by_id_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Users_by_Id_Todo'.
        ========================================================================
        """
        tname = 'users_by_id_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        return schema
    
    @staticmethod
    def users_by_id_unique_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Users_by_Id_Unique_Todo'.
        ========================================================================
        """
        tname = 'users_by_id_unique_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER_UNIQUE)
        return schema
    
    @staticmethod
    def videos_by_user() -> Schema:
        """
        ========================================================================
         Return schema for table 'Videos_by_User'.
        ========================================================================
        """ 
        tname = 'videos_by_user'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        schema.append(Fields.ID_MUSIC)
        schema.extend(Fields.video())
        schema.extend(Fields.audit())
        return schema   
    
    @staticmethod
    def videos_by_user_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Videos_by_User_Todo'.
        ========================================================================
        """ 
        tname = 'videos_by_user_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        return schema
    
    @staticmethod
    def videos_new_by_user() -> Schema:
        """
        ========================================================================
         Return schema for table 'Videos_New_by_User'.
        ========================================================================
        """ 
        tname = 'videos_new_by_user'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        schema.append(Fields.ID_MUSIC)
        schema.extend(Fields.video())
        schema.extend(Fields.audit())
        return schema   
    
    @staticmethod
    def videos_new_by_user_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Videos_New_by_User_Todo'.
        ========================================================================
        """ 
        tname = 'videos_new_by_user_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_USER)
        schema.append(Fields.CREATED)
        return schema
    
    @staticmethod
    def hashtags_by_keyword_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Hashtags_by_Keyword_Todo'.
        ========================================================================
        """ 
        tname = 'hashtags_by_keyword_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.KEYWORD)
        return schema
    
    @staticmethod
    def hashtags_by_keyword() -> Schema:
        """
        ========================================================================
         Return schema for table 'Hashtags_by_Keyword'.
        ========================================================================
        """
        tname = 'hashtags_by_keyword'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.KEYWORD)
        schema.extend(Fields.hashtag())
        schema.extend(Fields.audit())
        return schema
    
    @staticmethod
    def videos_by_hashtag_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Videos_by_Hashtag_Todo'.
        ========================================================================
        """
        tname = 'videos_by_hashtag_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_HASHTAG)
        return schema
    
    @staticmethod
    def videos_by_hashtag() -> Schema:
        """
        ========================================================================
         Return schema for table 'Videos_by_Hashtag'.
        ========================================================================
        """ 
        tname = 'videos_by_hashtag'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_HASHTAG)
        schema.extend(Fields.video())
        schema.extend(Fields.audit())
        return schema

    @staticmethod
    def music_by_id() -> Schema:
        """
        ========================================================================
         Return schema for table 'Musics_by_Id'.
        ========================================================================
        """
        tname = 'music_by_id'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_MUSIC)
        schema.append(Fields.TITLE)
        schema.append(Fields.AUTHOR)
        schema.append(Fields.DURATION)
        schema.append(Fields.IS_ORIGINAL)
        schema.append(Fields.VIDEOS)
        schema.append(Fields.PLAY)
        schema.extend(Fields.audit())
        return schema

    @staticmethod
    def music_by_id_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Musics_by_Id_Todo'.
        ========================================================================
        """
        tname = 'music_by_id_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_MUSIC)
        return schema
    
    @staticmethod
    def download_todo() -> Schema:
        """
        ========================================================================
         Return schema for table 'Download_Todo'.
        ========================================================================
        """
        tname = 'download_todo'
        schema = Schemas._create_schema(tname=tname)
        schema.append(Fields.ID_VIDEO)
        schema.append(Fields.PLAY)
        return schema
    
    @staticmethod
    def _create_schema(tname: str) -> Schema:
        """
        ========================================================================
         Create a schema for a given table.
        ========================================================================
        """
        name = Schemas._to_name(tname=tname)
        return Schema(name=name)

    @staticmethod
    def _to_name(tname: str) -> str:
        """
        ========================================================================
         Return a full name for a given table (with prefix).
        ========================================================================
        """ 
        return f'{Schemas._PRE}_{tname}'
