from f_google.client.base import ClientBase, Resource
from f_google.user import User
from googleapiclient.discovery import build


class ClientSlides(ClientBase):
    """
    ============================================================================
     Client for Google Slides.
    ============================================================================
    """

    def __init__(self, user: str = User.VALDAS) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(user=user)

    def _get_client(self) -> Resource:
        """
        ========================================================================
         Open and Return new Google-Slides-Client.
        ========================================================================
        """
        self._client = build('slides', 'v1', credentials=self.creds)
        return self._client

    def create_presentation(self, title: str) -> dict[str, str]:
        """
        ========================================================================
         Create a new presentation.
        ========================================================================
        """
        body = {'title': title}
        presentations = self._client.presentations()
        presentation = presentations().create(body=body)
        return presentation.execute()

    def get_black_background(self, slide: dict[str, str]) -> dict[str, str]:
        """
        ========================================================================
         Return a black background.
        ========================================================================
        """
        rgb_black = {'red': 0, 'green': 0, 'blue': 0}
        color = {'rgbColor': rgb_black}
        fill = {'solidFill': {'color': color}}
        properties = {'pageBackgroundFill': fill}
        object_id = slide['objectId']
        update = {'updatePageProperties': properties, 'objectId': object_id}
        return update
    
    def create_textbox(self, slide: dict[str, str], width) -> dict[str, str]:
