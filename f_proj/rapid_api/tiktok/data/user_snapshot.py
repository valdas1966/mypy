from dataclasses import dataclass


@dataclass
class DataUserSnapshot:
    """
    ============================================================================
     DataClass for User-Snapshot.
    ============================================================================
    """
    is_ok = bool
    is_found = bool
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
