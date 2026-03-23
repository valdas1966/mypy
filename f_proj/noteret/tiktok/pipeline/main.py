from f_proj.noteret.tiktok.pipeline._insert_parallel import insert_parallel
from f_proj.rapid_api.tiktok import ApiTikTok
from f_proj.noteret.tiktok.bq.tables import Tables
from typing import Any, Callable


class PipelineInsert:
    """
    ============================================================================
     Pipeline for Inserting TikTok API Data into BigQuery.
    ============================================================================
    """

    Factory: type = None

    _REGISTRY: dict[str, tuple[str, str, Callable[..., list[dict[str, Any]]]]] = {
        'videos_by_hashtag':  (Tables.VIDEOS_BY_HASHTAG,
                               Tables.VIDEOS_BY_HASHTAG_TODO,
                               ApiTikTok.videos_by_hashtag),
        'videos_by_user':     (Tables.VIDEOS_BY_USER,
                               Tables.VIDEOS_BY_USER_TODO,
                               ApiTikTok.videos_by_user),
        'videos_by_music':    (Tables.VIDEOS_BY_MUSIC,
                               Tables.VIDEOS_BY_MUSIC_TODO,
                               ApiTikTok.videos_by_music),
        'videos_new_by_user': (Tables.VIDEOS_NEW_BY_USER,
                               Tables.VIDEOS_NEW_BY_USER_TODO,
                               ApiTikTok.videos_new_by_user),
        'comments_by_video':  (Tables.COMMENTS_BY_VIDEO,
                               Tables.COMMENTS_BY_VIDEO_TODO,
                               ApiTikTok.comments_by_video),
        'followers_by_user':  (Tables.FOLLOWERS_BY_USER,
                               Tables.FOLLOWERS_BY_USER_TODO,
                               ApiTikTok.followers_by_user),
        'hashtags_by_keyword': (Tables.HASHTAGS_BY_KEYWORD,
                                Tables.HASHTAGS_BY_KEYWORD_TODO,
                                ApiTikTok.hashtags_by_keyword),
        'music_by_id':        (Tables.MUSIC_BY_ID,
                               Tables.MUSIC_BY_ID_TODO,
                               ApiTikTok.music_by_id),
        'users_by_id':        (Tables.USERS_BY_ID,
                               Tables.USERS_BY_ID_TODO,
                               ApiTikTok.users_by_id),
        'users_by_id_unique': (Tables.USERS_BY_ID,
                               Tables.USERS_BY_ID_UNIQUE_TODO,
                               ApiTikTok.users_by_id_unique),
    }

    @staticmethod
    def run(name: str, workers: int = 5) -> None:
        """
        ====================================================================
         Run parallel insert by name.
        ====================================================================
        """
        if name not in PipelineInsert._REGISTRY:
            names = ', '.join(sorted(PipelineInsert._REGISTRY))
            raise ValueError(
                f'Unknown name: {name}. Available: {names}')
        tname, tname_todo, func = PipelineInsert._REGISTRY[name]
        insert_parallel(tname=tname,
                        tname_todo=tname_todo,
                        func=func,
                        workers=workers)

    @staticmethod
    def names() -> list[str]:
        """
        ====================================================================
         Return all registered pipeline names.
        ====================================================================
        """
        return sorted(PipelineInsert._REGISTRY.keys())
