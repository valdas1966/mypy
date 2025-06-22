from google.cloud import videointelligence as vi
import old_f_google.inner.video_annotation.config as config


def video_context() -> vi.VideoContext:
    f = vi.VideoContext
    return f(speech_transcription_config=config.speech_transcription(),
             person_detection_config=config.person_detection(),
             face_detection_config=config.face_detection())
