from tenacity import retry, stop_after_attempt, wait_random_exponential
from google.cloud import videointelligence as vi
import old_f_google.inner.video_annotation.context as context


@retry(stop=stop_after_attempt(100),
       wait=wait_random_exponential(multiplier=1, max=30))
def run(json_key: str,
        uri_mp4: str,
        uri_json: str) -> None:
    features = [vi.Feature.LOGO_RECOGNITION,
                vi.Feature.TEXT_DETECTION]
    request ={'input_uri': uri_mp4,
              'output_uri': uri_json,
              'features': features,
              'video_context': context.video_context()}
    service = vi.VideoIntelligenceServiceClient
    from_file = service.from_service_account_file
    client = from_file(json_key)
    operation = client.annotate_video(request=request)
    operation.result(timeout=3000)
