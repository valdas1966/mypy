from f_proj.rapid_api.tiktok.requests import RequestsTiktok
from typing import Any


def user_by_id(id_user: str) -> list[dict[str, Any]]:
    """
    ========================================================================
        Generate user by id.
    ========================================================================
    """
    return RequestsTiktok.users_by_id(id_user=id_user)


def user_by_id_unique(id_user_unique: str) -> list[dict[str, Any]]:
    """
    ========================================================================
        Generate user by id unique.
    ========================================================================
    """
    return RequestsTiktok.users_by_id_unique(id_user_unique=id_user_unique)


def videos_by_user(id_user: str) -> list[dict[str, Any]]:
    """
    ========================================================================
        Generate videos by user.
    ========================================================================
    """
    return RequestsTiktok.videos_by_user(id_user=id_user)


def hashtags_by_keyword(keyword: str) -> list[dict[str, Any]]:
    """
    ========================================================================
        Generate hashtags by keyword.
    ========================================================================
    """
    return RequestsTiktok.hashtags_by_keyword(keyword=keyword)
