from f_google.services.slides.client import ClientSlides
from f_google.user import User


class GenClientSlides:

    @staticmethod
    def gen_valdas() -> ClientSlides:
        """
        ========================================================================
         Generate new Client-Slides.
        ========================================================================
        """
        return ClientSlides(user=User.VALDAS)


slides = GenClientSlides.gen_valdas()
print(slides.user)
print(slides.creds.project_id)
print(type(slides._client))
