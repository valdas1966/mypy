from dataclasses import dataclass


@dataclass
class DataUserInfo:
    """
    ============================================================================
     DataClass for UserInfo.
    ============================================================================
    """
    source = str
    id_user = str
    nick = str
    is_verified = bool
    is_secret = bool
    is_private = bool
    following = int
    followers = int
    videos = int
    hearts = int
    diggs = int
