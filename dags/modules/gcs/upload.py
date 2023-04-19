from google.cloud import storage


def json_string(project_id: str,
                bucket: str,
                json_name: str,
                json_str: str):
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(json_name)
    blob.upload_from_string(json_str, content_type='application/json')
