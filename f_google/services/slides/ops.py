from f_google.services.slides.client import ClientSlides, Resource


class Ops:
    """
    =========================================================================
     Operations for Google-Slides.
    =========================================================================
    """

    @staticmethod
    def get_client() -> Resource:
        """
        ========================================================================
         Get Google-Slides-Client.
        ========================================================================
        """
        return ClientSlides().client
    

