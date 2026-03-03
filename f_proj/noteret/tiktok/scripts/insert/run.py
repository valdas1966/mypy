from f_proj.noteret.tiktok.scripts.insert._insert_parallel import insert_parallel
from f_proj.rapid_api.tiktok.requests import RequestsTiktok
from f_proj.noteret.tiktok.tables import Tables
import sys


_REGISTRY = {
    'videos_by_hashtag': (Tables.VIDEOS_BY_HASHTAG,
                          Tables.VIDEOS_BY_HASHTAG_TODO,
                          RequestsTiktok.videos_by_hashtag),
    'videos_by_user':    (Tables.VIDEOS_BY_USER,
                          Tables.VIDEOS_BY_USER_TODO,
                          RequestsTiktok.videos_by_user),
    'videos_by_music':   (Tables.VIDEOS_BY_MUSIC,
                          Tables.VIDEOS_BY_MUSIC_TODO,
                          RequestsTiktok.videos_by_music),
    'videos_new_by_user': (Tables.VIDEOS_NEW_BY_USER,
                           Tables.VIDEOS_NEW_BY_USER_TODO,
                           RequestsTiktok.videos_new_by_user),
    'comments_by_video': (Tables.COMMENTS_BY_VIDEO,
                          Tables.COMMENTS_BY_VIDEO_TODO,
                          RequestsTiktok.comments_by_video),
    'followers_by_user': (Tables.FOLLOWERS_BY_USER,
                          Tables.FOLLOWERS_BY_USER_TODO,
                          RequestsTiktok.followers_by_user),
    'hashtags_by_keyword': (Tables.HASHTAGS_BY_KEYWORD,
                            Tables.HASHTAGS_BY_KEYWORD_TODO,
                            RequestsTiktok.hashtags_by_keyword),
    'music_by_id':       (Tables.MUSIC_BY_ID,
                          Tables.MUSIC_BY_ID_TODO,
                          RequestsTiktok.music_by_id),
    'users_by_id':       (Tables.USERS_BY_ID,
                          Tables.USERS_BY_ID_TODO,
                          RequestsTiktok.users_by_id),
    'users_by_id_unique': (Tables.USERS_BY_ID,
                           Tables.USERS_BY_ID_UNIQUE_TODO,
                           RequestsTiktok.users_by_id_unique),
}


def run(name: str, workers: int = 5) -> None:
    """
    ========================================================================
     Run parallel insert by name.
    ========================================================================
    """
    if name not in _REGISTRY:
        names = ', '.join(sorted(_REGISTRY))
        raise ValueError(f'Unknown name: {name}. Available: {names}')
    tname, tname_todo, func = _REGISTRY[name]
    insert_parallel(tname=tname,
                    tname_todo=tname_todo,
                    func=func,
                    workers=workers)


# Set _NAME and _WORKERS for PyCharm, or pass as CLI arguments
_NAME = 'videos_by_hashtag'
_WORKERS = 16

if len(sys.argv) > 1:
    _NAME = sys.argv[1]
if len(sys.argv) > 2:
    _WORKERS = int(sys.argv[2])
run(name=_NAME, workers=_WORKERS)
