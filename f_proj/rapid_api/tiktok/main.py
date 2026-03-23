from f_proj.rapid_api.tiktok.endpoints.i_1_users_by_id import EndpointUsersById
from f_proj.rapid_api.tiktok.endpoints.i_1_users_by_id_unique import EndpointUsersByIdUnique
from f_proj.rapid_api.tiktok.endpoints.i_1_videos_by_user import EndpointVideosByUser
from f_proj.rapid_api.tiktok.endpoints.i_1_videos_new_by_user import EndpointVideosNewByUser
from f_proj.rapid_api.tiktok.endpoints.i_1_hashtags_by_keyword import EndpointHashtagsByKeyword
from f_proj.rapid_api.tiktok.endpoints.i_1_videos_by_hashtag import EndpointVideosByHashtag
from f_proj.rapid_api.tiktok.endpoints.i_1_followers_by_user import EndpointFollowersByUser
from f_proj.rapid_api.tiktok.endpoints.i_1_music_by_id import EndpointMusicById
from f_proj.rapid_api.tiktok.endpoints.i_1_videos_by_music import EndpointVideosByMusic
from f_proj.rapid_api.tiktok.endpoints.i_1_comments_by_video import EndpointCommentsByVideo
from typing import Any


class ApiTikTok:
    """
    ============================================================================
     Public API for TikTok on RapidAPI.
    ============================================================================
    """

    @staticmethod
    def users_by_id(id_user: str) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch users by their ids.
        ====================================================================
        """
        return EndpointUsersById(id_user=id_user).run()

    @staticmethod
    def users_by_id_unique(id_user_unique: str
                           ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch users by their unique ids.
        ====================================================================
        """
        return EndpointUsersByIdUnique(
            id_user_unique=id_user_unique).run()

    @staticmethod
    def videos_by_user(id_user: str,
                       limit: int = None
                       ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch videos by user id.
        ====================================================================
        """
        return EndpointVideosByUser(
            id_user=id_user).run(limit=limit)

    @staticmethod
    def videos_new_by_user(id_user: str,
                           created: str
                           ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch videos by user id (only after timestamp).
        ====================================================================
        """
        return EndpointVideosNewByUser(
            id_user=id_user, created=created).run()

    @staticmethod
    def hashtags_by_keyword(keyword: str,
                            limit: int = None
                            ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch hashtags by keyword.
        ====================================================================
        """
        return EndpointHashtagsByKeyword(
            keyword=keyword).run(limit=limit)

    @staticmethod
    def videos_by_hashtag(id_hashtag: str,
                          limit: int = None
                          ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch videos by hashtag id.
        ====================================================================
        """
        return EndpointVideosByHashtag(
            id_hashtag=id_hashtag).run(limit=limit)

    @staticmethod
    def followers_by_user(id_user: str,
                          limit: int = None
                          ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch followers by user id.
        ====================================================================
        """
        return EndpointFollowersByUser(
            id_user=id_user).run(limit=limit)

    @staticmethod
    def music_by_id(id_music: str) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch music by id.
        ====================================================================
        """
        return EndpointMusicById(id_music=id_music).run()

    @staticmethod
    def videos_by_music(id_music: str,
                        limit: int = None
                        ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch videos by music id.
        ====================================================================
        """
        return EndpointVideosByMusic(
            id_music=id_music).run(limit=limit)

    @staticmethod
    def comments_by_video(id_video: str,
                          limit: int = None
                          ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch comments by video id.
        ====================================================================
        """
        return EndpointCommentsByVideo(
            id_video=id_video).run(limit=limit)
