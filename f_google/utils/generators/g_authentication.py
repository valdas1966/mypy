from f_google.utils.u_authentication import UAuthentication, Credentials
from f_google.user import User



class GenAuthentication:
    """
    ============================================================================
     Generators for user's authentication (credentials).
    ============================================================================
    """

    @staticmethod
    def gen_rami() -> Credentials:
        """
        ============================================================================
         Generate Rami's Authentication (Credentials).
        ============================================================================
        """
        user = User.RAMI
        return UAuthentication.get(user=user)

    @staticmethod
    def gen_user() -> Credentials:
        """
        ============================================================================
         Generate user's Authentication (Credentials).
        ============================================================================
        """
        user = User.VALDAS
        return UAuthentication.get(user=user)


rami = GenAuthentication.gen_rami()
print(type(rami))
print(rami.project_id)

valdas = GenAuthentication.gen_user()
print(type(valdas))
print(valdas.project_id)

