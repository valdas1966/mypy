from google.cloud import videointelligence
from collections import Counter
import os
from f_utils import u_datetime
from f_logging.dec import log_info


@log_info
def get_annotations(str_bucket: str,
                    id_video: str) -> list[dict]:
    bucket = f'gs://{str_bucket}'
    annotations = __mp4_to_annotations(bucket=bucket, id_video=id_video)
    return __annotations_to_dicts(id_video=id_video, annotations=annotations)


@log_info
def __mp4_to_annotations(bucket, id_video):
    json_key = 'd:\\professor\\gcp\\owner.json'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_key
    path_mp4 = f'{bucket}/mp4/{id_video}.mp4'
    client = videointelligence.VideoIntelligenceServiceClient()
    features = ['LABEL_DETECTION']
    job = client.annotate_video(input_uri=path_mp4, features=features)
    return job.result()


@log_info
def __annotations_to_dicts(id_video: str,
                           annotations) -> dict:
    res = annotations.annotation_results[0]
    segment = res.segment_label_annotations
    c_segment = Counter([x.entity.description for x in segment])
    shot = res.shot_label_annotations
    c_shot = Counter([x.entity.description for x in shot])
    c_all = c_segment + c_shot
    inserted = u_datetime.now()
    return [{'inserted': inserted,
             'id_video': id_video,
             'annotation': annotaion,
             'cnt': cnt}
            for annotaion, cnt in c_all.items()]

"""
str_bucket = 'tiktok_movies'
id_video = '160782035354181632'
id_video = '6885437744437382401'
x = get_annotations(id_video=id_video, str_bucket=str_bucket)
print(x)
"""
