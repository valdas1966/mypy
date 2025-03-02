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
        return TiktokAPI.users_by_id(id_user)


d = GenTiktokAPI.user_by_id()
print(d)

"""
{
    'id_user': <built-in function id>,
     'is_ok': True,
      'is_found': True,
       'id_user_unique': 'tiktok',
        'nick': 'TikTok',
         'is_verified': True,
          'is_secret': False,
           'is_private': False,
            'following': 1,
             'followers': 88720567,
              'videos': 1174,
               'hearts': 357588856,
                'diggs': 0,
                 'is_broken': False}
"""
