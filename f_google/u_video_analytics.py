from google.cloud import videointelligence
from collections import Counter
import os
from tenacity import retry, stop_after_attempt, wait_random_exponential


def get_annotations(json_key: str,
                    str_bucket: str,
                    id_video: str) -> list[dict]:
    bucket = f'gs://{str_bucket}'
    annotations = __mp4_to_annotations(json_key=json_key,
                                       bucket=bucket,
                                       id_video=id_video)
    return __annotations_to_dicts(id_video=id_video, annotations=annotations)


@retry(stop=stop_after_attempt(100), wait=wait_random_exponential(
    multiplier=1, max=60))
def __mp4_to_annotations(json_key: str,
                         bucket: str,
                         id_video: str) -> 'list of dict':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_key
    path_mp4 = f'{bucket}/{id_video}.mp4'
    client = videointelligence.VideoIntelligenceServiceClient()
    features = ['LABEL_DETECTION']
    job = client.annotate_video(input_uri=path_mp4, features=features)
    return job.result()


def __annotations_to_dicts(id_video: str,
                           annotations) -> dict:
    res = annotations.annotation_results[0]
    segment = res.segment_label_annotations
    c_segment = Counter([x.entity.description for x in segment])
    shot = res.shot_label_annotations
    c_shot = Counter([x.entity.description for x in shot])
    c_all = c_segment + c_shot
    c_clean = {k.replace('\'', '').replace('\"', ''): v
               for k, v in c_all.items()}
    return [{'id_video': id_video,
             'annotation': annotaion,
             'cnt': cnt}
            for annotaion, cnt in c_clean.items()]


"""
json_key = 'd:\\tiktok\\repo\\viewer.json'
str_bucket = 'noteret_mp4'
id_video = '7075396968930954497'
a = get_annotations(json_key=json_key, str_bucket=str_bucket, id_video=id_video)
print(a)
"""