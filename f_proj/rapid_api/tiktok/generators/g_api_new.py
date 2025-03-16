from f_proj.rapid_api.tiktok.api_new import TiktokAPI
from typing import Any


class GenTiktokAPI:
    """
    ============================================================================
     Class for generating TikTok API.
    ============================================================================
    """

    @staticmethod
    def user_by_id() -> dict[str, Any]:
        """
        ========================================================================
         Generate user by id.
        ========================================================================
        """ 
        id_user = '107955'
        return TiktokAPI.users_by_id(id_user=id_user)
    
    @staticmethod   
    def user_by_id_unique() -> dict[str, Any]:
        """
        ========================================================================
         Generate user by id unique.
        ========================================================================
        """
        id_user_unique = 'tiktok'
        return TiktokAPI.users_by_id_unique(id_user_unique=id_user_unique)
    
    @staticmethod   
    def videos_by_user() -> list[dict[str, Any]]:
        """
        ========================================================================
         Generate videos by user.
        ========================================================================
        """
        # id_user = '7164667879018021914'
        id_user = '7125301884189426693'
        return TiktokAPI.videos_by_user(id_user)


# print(GenTiktokAPI.user_by_id())
print(GenTiktokAPI.user_by_id_unique())
