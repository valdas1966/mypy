from old_f_google.user import User


class GenUser:
    """
    ============================================================================
     Generate the old_path to the JSON files for the users.
    ============================================================================
    """ 

    @staticmethod
    def gen_rami() -> str:
        """
        ============================================================================
         Generate the old_path to the Rami's JSON file.
        ============================================================================
        """
        return User.RAMI
    
    @staticmethod
    def gen_valdas() -> str:
        """
        ============================================================================
         Generate the old_path to the Valdas' JSON file.
        ============================================================================
        """ 
        return User.VALDAS


rami = GenUser.gen_rami()
print(type(rami))
print(rami)
print()

valdas = GenUser.gen_valdas()
print(type(valdas))
print(valdas)