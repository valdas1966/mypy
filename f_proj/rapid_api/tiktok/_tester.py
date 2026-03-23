from f_proj.rapid_api.tiktok import ApiTikTok
from f_proj.rapid_api.tiktok._factory import Factory
import pytest


# =========================================================================
#  Schema Validator
# =========================================================================

def _assert_schema(row: dict,
                   schema: dict[str, type]) -> None:
    """
    ========================================================================
     Validate that a row matches the expected type schema.
    ========================================================================
    """
    missing = set(schema.keys()) - set(row.keys())
    assert not missing, f'Missing keys: {missing}'
    extra = set(row.keys()) - set(schema.keys())
    assert not extra, f'Unexpected keys: {extra}'
    for key, expected_type in schema.items():
        val = row[key]
        assert isinstance(val, expected_type), (
            f'{key}: expected {expected_type.__name__}, '
            f'got {type(val).__name__} ({val!r})')


# =========================================================================
#  Fixtures — volatile IDs fetched live from the API
# =========================================================================

@pytest.fixture(scope='module')
def video_row() -> dict:
    """
    ========================================================================
     Fetch a fresh video from @tiktok (stable user, volatile video).
    ========================================================================
    """
    rows = ApiTikTok.videos_by_user(id_user=Factory.ID_USER,
                                    limit=1)
    assert len(rows) >= 1 and rows[0].get('is_ok'), \
        'Failed to fetch a video from @tiktok'
    return rows[0]


@pytest.fixture(scope='module')
def id_video(video_row: dict) -> str:
    """
    ========================================================================
     A live video ID from @tiktok.
    ========================================================================
    """
    return video_row['id_video']


@pytest.fixture(scope='module')
def id_music(video_row: dict) -> str:
    """
    ========================================================================
     A live music ID from a @tiktok video.
    ========================================================================
    """
    return video_row['id_music']


# =========================================================================
#  Tests
# =========================================================================

def test_users_by_id() -> None:
    """
    ============================================================================
     Test fetching a user by numeric ID.
    ============================================================================
    """
    rows = ApiTikTok.users_by_id(id_user=Factory.ID_USER)
    assert len(rows) == 1
    row = rows[0]
    _assert_schema(row=row, schema=Factory.SCHEMA_USER_BY_ID)
    # Stable values for @tiktok
    assert row['id_user'] == Factory.ID_USER
    assert row['nick'] == 'TikTok'
    assert row['is_verified'] is True
    assert row['is_private'] is False


def test_users_by_id_unique() -> None:
    """
    ============================================================================
     Test fetching a user by unique ID.
    ============================================================================
    """
    rows = ApiTikTok.users_by_id_unique(
        id_user_unique=Factory.ID_USER_UNIQUE)
    assert len(rows) == 1
    row = rows[0]
    _assert_schema(row=row,
                   schema=Factory.SCHEMA_USER_BY_ID_UNIQUE)
    # Stable values for @tiktok
    assert row['id_user_unique'] == Factory.ID_USER_UNIQUE
    assert row['id_user'] == Factory.ID_USER
    assert row['nick'] == 'TikTok'
    assert row['is_verified'] is True
    assert row['is_found'] is True


def test_videos_by_user() -> None:
    """
    ============================================================================
     Test fetching videos by user ID (limit=2).
    ============================================================================
    """
    rows = ApiTikTok.videos_by_user(id_user=Factory.ID_USER,
                                    limit=2)
    assert len(rows) >= 1
    for row in rows:
        _assert_schema(row=row, schema=Factory.SCHEMA_VIDEO)
        assert row['id_user'] == Factory.ID_USER


def test_hashtags_by_keyword() -> None:
    """
    ============================================================================
     Test fetching hashtags by keyword (limit=2).
    ============================================================================
    """
    rows = ApiTikTok.hashtags_by_keyword(keyword=Factory.KEYWORD,
                                         limit=2)
    assert len(rows) >= 1
    for row in rows:
        _assert_schema(row=row, schema=Factory.SCHEMA_HASHTAG)
        assert row['keyword'] == Factory.KEYWORD


def test_videos_by_hashtag() -> None:
    """
    ============================================================================
     Test fetching videos by hashtag ID (limit=2).
    ============================================================================
    """
    rows = ApiTikTok.videos_by_hashtag(
        id_hashtag=Factory.ID_HASHTAG, limit=2)
    assert len(rows) >= 1
    for row in rows:
        _assert_schema(row=row,
                       schema=Factory.SCHEMA_VIDEO_BY_HASHTAG)
        assert row['id_hashtag'] == Factory.ID_HASHTAG


def test_followers_by_user() -> None:
    """
    ============================================================================
     Test fetching followers by user ID (limit=2).
    ============================================================================
    """
    rows = ApiTikTok.followers_by_user(id_user=Factory.ID_USER,
                                       limit=2)
    assert len(rows) >= 1
    for row in rows:
        _assert_schema(row=row, schema=Factory.SCHEMA_FOLLOWER)
        assert row['id_user'] == Factory.ID_USER


def test_music_by_id(id_music: str) -> None:
    """
    ============================================================================
     Test fetching music by ID (live ID from fixture).
    ============================================================================
    """
    rows = ApiTikTok.music_by_id(id_music=id_music)
    assert len(rows) == 1
    row = rows[0]
    _assert_schema(row=row, schema=Factory.SCHEMA_MUSIC)
    assert row['id_music'] == id_music


def test_videos_by_music(id_music: str) -> None:
    """
    ============================================================================
     Test fetching videos by music ID (live ID from fixture).
    ============================================================================
    """
    rows = ApiTikTok.videos_by_music(id_music=id_music,
                                     limit=2)
    assert len(rows) >= 1
    for row in rows:
        _assert_schema(row=row,
                       schema=Factory.SCHEMA_VIDEO_BY_MUSIC)
        assert row['id_music'] == id_music


def test_comments_by_video(id_video: str) -> None:
    """
    ============================================================================
     Test fetching comments by video ID (live ID from fixture).
    ============================================================================
    """
    rows = ApiTikTok.comments_by_video(id_video=id_video,
                                       limit=2)
    assert len(rows) >= 1
    for row in rows:
        _assert_schema(row=row, schema=Factory.SCHEMA_COMMENT)
        assert row['id_video'] == id_video
