from old_f_google.services.slides.client import ClientSlides
from googleapiclient.discovery import build
from old_f_google.services.slides.ops import Ops
from typing import Any


def create_test_slide():
    """
    ========================================================================
     Create a new test-slide.
    ========================================================================
    """
    gs = ClientSlides()
    
    # Create a new presentation with the desired title.
    presentation = gs.create_presentation(title='Test')
    
    # Get the first (default) slide's ID.
    slide = presentation['slides'][0]
    
    # Prepare batch update requests.
    requests: list[dict[str, Any]] = list()
    
    # Update the slide background to solid black.
    background = gs.get_black_background(slide=slide)
    requests.append(background)
           
    # 3b. Create a text box shape for the text.
    textbox_id = "MyTextBox_01"
    # Here we assume the slide is 960 PT wide and 540 PT tall.
    # We create a 300x100 PT textbox and position it roughly at the center.
    requests.append({
        "createShape": {
            "objectId": textbox_id,
            "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": sid,
                "size": {
                    "width": {"magnitude": 300, "unit": "PT"},
                    "height": {"magnitude": 100, "unit": "PT"}
                },
                "transform": {
                    "scaleX": 1,
                    "scaleY": 1,
                    "translateX": 330,  # (960-300)/2
                    "translateY": 220,  # (540-100)/2
                    "unit": "PT"
                }
            }
        }
    })
    
    # 3c. Insert the text "TEST" into the text box.
    requests.append({
        "insertText": {
            "objectId": textbox_id,
            "insertionIndex": 0,
            "text": "TEST"
        }
    })
    
    # 3d. Update the text style: set font size to 48 PT, white color, and bold.
    requests.append({
        "updateTextStyle": {
            "objectId": textbox_id,
            "style": {
                "fontSize": {"magnitude": 48, "unit": "PT"},
                "foregroundColor": {
                    "opaqueColor": {
                        "rgbColor": {"red": 1, "green": 1, "blue": 1}
                    }
                },
                "bold": True
            },
            "textRange": {"type": "ALL"},
            "fields": "fontSize,foregroundColor,bold"
        }
    })
    
    # 3e. Center-align the text within the text box.
    requests.append({
        "updateParagraphStyle": {
            "objectId": textbox_id,
            "style": {
                "alignment": "CENTER",
                "contentAlignment": "MIDDLE"
            },
            "textRange": {"type": "ALL"}, 
            "fields": "alignment,contentAlignment"
        }
    })
    
    # 4. Execute the batch update.
    body = {"requests": requests}
    response = gslides.presentations().batchUpdate(
        presentationId=pid, body=body).execute()
    print(response)

    # Assuming you already have your service account credentials in `creds`
    drive_service = build('drive', 'v3', credentials=client.creds)

    permission = {
        'type': 'user',
        'role': 'writer',  # or 'reader'
        'emailAddress': 'valdas.ivanauskas.1966@gmail.com'
    }

    drive_service.permissions().create(
        fileId=pid,
        body=permission,
        fields='id'
    ).execute()


if __name__ == '__main__':
    create_test_slide()
