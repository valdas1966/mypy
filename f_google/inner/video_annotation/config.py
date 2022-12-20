from google.cloud import videointelligence as vi


def speech_transcription() -> vi.SpeechTranscriptionConfig:
    """
    ============================================================================
     Description: Return Speech-Transcription Configuration.
    ============================================================================
    """
    f = vi.SpeechTranscriptionConfig
    return f(language_code='en-US',
             enable_automatic_punctuation=True)


def person_detection() -> vi.PersonDetectionConfig:
    """
    ============================================================================
     Description: Return Person-Detection Configuration.
    ============================================================================
    """
    f = vi.PersonDetectionConfig
    return f(include_bounding_boxes=True,
             include_attributes=False,
             include_pose_landmarks=True)


def face_detection() -> vi.FaceDetectionConfig:
    """
    ============================================================================
     Description: Return Face-Detection Configuration.
    ============================================================================
    """
    f = vi.FaceDetectionConfig
    return f(include_bounding_boxes=True,
             include_attributes=True)
