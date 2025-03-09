from f_proj.rapid_api.data.i_2_users_by_id import DataUsersById


class GenUsersById:
    """
    ============================================================================
     Generator for request 'Users by ID'.
    ============================================================================
    """
    
    @staticmethod
    def custom() -> DataUsersById:
        """
        ============================================================================
         Custom generator for request 'Users by ID'.
        ============================================================================
        """
        response = {'code': 200,
                    'data': {'user': {'user_id': '123'},
                             'stats': {'video_count': 100}
                             }
                    }
        data = DataUsersById()
        data.is_ok = True
        data.fill(**response)
        return data


data = GenUsersById.custom()
d = data.to_flat_dict()
print(d)
