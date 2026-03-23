from f_google.services.gemini.main import Gemini
from f_google.creds.auth import Auth


class Factory:
    """
    ========================================================================
     Factory for Gemini Client.
    ========================================================================
    """

    @staticmethod
    def rami(model: str = None) -> Gemini:
        """
        ====================================================================
         Return a Gemini Client with RAMI SA Credentials.
        ====================================================================
        """
        creds = Auth.Factory.rami()
        return Gemini(creds=creds, model=model)
