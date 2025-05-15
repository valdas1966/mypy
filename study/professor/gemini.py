import os
import time
import json
import re
import warnings
import logging

from google.cloud import storage, bigquery
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError

import vertexai
from vertexai.generative_models import GenerativeModel, Part

# === CONFIG ===
project_id = "noteret1"
location = "us-central1"
service_account_key_path = r'd:\jsons\noteret_1.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key_path

input_bucket_name = 'noteret_mp4_standard'
batch_bucket_name = f"{project_id}_batch_inserts"
table_id = 'noteret.vtt.itai_2025_05_01_video_analyzed'

# === Disable noisy logs ===
logging.getLogger().setLevel(logging.CRITICAL)
for lib in ["google", "google.cloud", "google.auth"]:
    logging.getLogger(lib).setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore", category=UserWarning)

# === Setup ===
print("[INFO] Initializing clients...")

try:
    vertexai.init(project=project_id, location=location)
    bq_client = bigquery.Client(project=project_id)
    storage_client = storage.Client(project=project_id)
    print("[SUCCESS] Setup completed successfully.")
except Exception as e:
    print(f"[ERROR] Setup failed: {e}")
    exit(1)

# === Model ===
model = GenerativeModel("gemini-2.0-flash")

# === Schema ===
schema = [
    bigquery.SchemaField("file_name", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("index_depart", "INT64"),
    bigquery.SchemaField("index_depart_explained", "STRING"),
    bigquery.SchemaField("index_military", "INT64"),
    bigquery.SchemaField("index_military_explained", "STRING"),
    bigquery.SchemaField("index_woman", "INT64"),
    bigquery.SchemaField("index_woman_explained", "STRING"),
]

# === Create table if needed ===
def create_table_if_not_exists():
    try:
        bq_client.get_table(table_id)
        print(f"[INFO] Table `{table_id}` exists.")
    except:
        print(f"[INFO] Creating table `{table_id}`...")
        table = bigquery.Table(table_id, schema=schema)
        bq_client.create_table(table)
        print("[SUCCESS] Table created.")

create_table_if_not_exists()

# === Utility Functions ===

def get_processed_files():
    print("[INFO] Fetching list of already processed files...")
    try:
        query = f"SELECT DISTINCT file_name FROM `{table_id}`"
        return {row.file_name for row in bq_client.query(query)}
    except Exception as e:
        print(f"[ERROR] Failed to fetch processed files: {e}")
        return set()

def get_videos_to_process():
    print("[INFO] Fetching list of videos to process...")
    try:
        query = """
            SELECT DISTINCT id_video FROM `noteret.json_load.id_video_assignment`
            WHERE cat = 1
        """
        return {row.id_video if row.id_video.endswith(".mp4") else f"{row.id_video}.mp4"
                for row in bq_client.query(query)}
    except Exception as e:
        print(f"[ERROR] Failed to fetch videos to process: {e}")
        return set()

def delay_request():
    global last_request_time, request_count
    now = time.time()
    if request_count >= max_requests_per_minute:
        wait = max(0, time_interval - (now - last_request_time))
        print(f"[INFO] Rate limit hit. Waiting {wait:.1f} seconds...")
        if wait > 0:
            time.sleep(wait)
        request_count = 0
        last_request_time = time.time()
    request_count += 1

def generate_content_with_backoff(video_part, prompt, retries=3, backoff_factor=2):
    for attempt in range(retries):
        try:
            return model.generate_content(
                [video_part, prompt],
                generation_config={"max_output_tokens": 1000, "temperature": 0}
            )
        except ResourceExhausted:
            print(f"[WARNING] Quota exceeded (attempt {attempt+1})")
            if attempt < retries - 1:
                time.sleep(backoff_factor ** attempt)
        except GoogleAPICallError as e:
            print(f"[ERROR] API error: {e}")
            raise

def try_parse_json_array(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception as e:
                print(f"[ERROR] Regex parse failed: {e}")
    return None

# === Prompt ===
prompt = """..."""  # Keep your original full prompt here

# === Main Execution ===
print("[INFO] Starting main processing loop...")

processed_files = get_processed_files()
videos_to_process = get_videos_to_process()
print(f"[INFO] {len(videos_to_process)} videos to process, {len(processed_files)} already processed.")

input_bucket = storage_client.bucket(input_bucket_name)
batch_bucket = storage_client.bucket(batch_bucket_name)

if not batch_bucket.exists():
    storage_client.create_bucket(batch_bucket)
    print(f"[INFO] Created batch bucket: {batch_bucket_name}")

# Rate limiting config
request_count = 0
max_requests_per_minute = 9
time_interval = 60
last_request_time = time.time()

# Process each video
for blob in input_bucket.list_blobs():
    if not blob.name.endswith('.mp4'):
        continue
    if blob.name not in videos_to_process:
        print(f"[SKIP] {blob.name} is not in video list.")
        continue
    if blob.name in processed_files:
        print(f"[SKIP] {blob.name} already processed.")
        continue

    print(f"[PROCESSING] {blob.name}")
    delay_request()

    try:
        video_content = blob.download_as_bytes()
        video_part = Part.from_data(data=video_content, mime_type="video/mp4")

        print("[INFO] Calling Gemini...")
        response = generate_content_with_backoff(video_part, prompt)

        print("[INFO] Parsing Gemini response...")
        json_result = try_parse_json_array(response.text)

        if not json_result:
            print(f"[WARNING] Could not parse JSON for {blob.name}")
            continue

        print(f"[INFO] Total rows to insert: {len(json_result)}")
        for i, row in enumerate(json_result):
            print(f"\n--- Row {i+1} for file: {blob.name} ---")
            print(json.dumps(row, indent=2, ensure_ascii=False))
            print("--- End of Row ---")

        print("[INFO] Inserting into BigQuery now...")
        bq_client.insert_rows_json(table_id, json_result)

        print("[INFO] Backing up result to batch bucket...")
        batch_blob = batch_bucket.blob(f"{blob.name}.json")
        batch_blob.upload_from_string(json.dumps(json_result, ensure_ascii=False), content_type="application/json")

        print(f"[SUCCESS] Finished processing {blob.name}")

    except Exception as e:
        print(f"[ERROR] Failed to process {blob.name}: {e}")
