import time
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage, bigquery
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Vertex AI
vertexai.init(project='noteret', location="us-central1")

# Initialize the generative model (Gemini)
model = GenerativeModel("gemini-2.0-flash-exp")

# Define the bucket name and BigQuery table
input_bucket_name = 'bucket_contents_1_percent_records'
table_id = 'noteret.vtt.graves_detected'

# Set up Google Cloud clients
storage_client = storage.Client()
bq_client = bigquery.Client()

# Define schema for BigQuery table
schema = [
    bigquery.SchemaField("file_name", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("cemetery_seen_indicator", "BOOL"),
    bigquery.SchemaField("photo_on_grave_seen_indicator", "BOOL"),
    bigquery.SchemaField("martyr_seen_indicator", "BOOL"),
]


# Ensure the table exists
def create_table_if_not_exists():
    try:
        bq_client.get_table(table_id)
        logging.info("Table already exists.")
    except Exception:
        logging.info("Table does not exist. Creating table...")
        table = bigquery.Table(table_id, schema=schema)
        bq_client.create_table(table)
        logging.info("Table created.")


create_table_if_not_exists()


# Retrieve existing file names from BigQuery table
def get_processed_files():
    try:
        query = f"SELECT file_name FROM `{table_id}`"
        query_job = bq_client.query(query)
        processed_files = {row.file_name for row in query_job}
        logging.info(
            f"Retrieved {len(processed_files)} already-processed files.")
        return processed_files
    except Exception as e:
        logging.error(f"Error retrieving processed files: {e}")
        return set()


# Fetch already processed files
processed_files = get_processed_files()

# Get the input bucket and list blobs
input_bucket = storage_client.bucket(input_bucket_name)
blobs = input_bucket.list_blobs()

request_count = 0
max_requests_per_minute = 9
time_interval = 60  # 60 seconds per minute
last_request_time = time.time()


# Delay requests to avoid quota limits
def delay_request():
    global last_request_time, request_count
    current_time = time.time()

    if request_count >= max_requests_per_minute:
        time_since_last_request = current_time - last_request_time
        if time_since_last_request < time_interval:
            time.sleep(time_interval - time_since_last_request)
            request_count = 0
            last_request_time = time.time()


# Exponential backoff for quota errors
def generate_content_with_backoff(video_part, prompt, retries=3,
                                  backoff_factor=2):
    for attempt in range(retries):
        try:
            response = model.generate_content(
                [video_part, prompt],
                generation_config={"max_output_tokens": 1000, "temperature": 0}
            )
            return response
        except ResourceExhausted as e:
            logging.warning(
                f"Quota exceeded, retrying... Attempt {attempt + 1}/{retries}")
            if attempt < retries - 1:
                time.sleep(backoff_factor ** attempt)
            else:
                raise e
        except GoogleAPICallError as e:
            logging.error(f"API call failed: {e}")
            raise e


# Process each video
for blob in blobs:
    if blob.name.endswith('.mp4'):
        # Skip if file has already been processed
        if blob.name in processed_files:
            logging.info(f"Skipping already processed video: {blob.name}")
            continue

        logging.info(f"Processing started for video: {blob.name}")

        delay_request()

        try:
            video_content = blob.download_as_bytes()
            video_part = Part.from_data(data=video_content,
                                        mime_type="video/mp4")

            prompt = (
                "Goal: Transform each video file in the input bucket into a record organized as five distinct fields. "
                "Later on, we will insert these records into a BigQuery table. Each video-file must correspond to one--and only one--record. "
                "These records must include only English words. The desired structured format of each record is: "
                "(1) file_name: The video's file name without the suffix. "
                "(2) description: A summary that captures the essential information of the video. If the video contains frames from a cemetery, include in your description english translations of what is written on the graves and what the images on the grave are. Include only positive statements such as 'An image of a a head appears on a grave'. Do not include negative statemnts such as 'image not on grave'. Include in your summary an English translation of all the text that appears in the video. An example of a good description is: 'The video shows a cemetery with many graves. A group of people are seen in the background. The text on the screen says Death will come and end all the sorrows of life'. "
                "(3) cemetery_seen_indicator: TRUE or FALSE if a cemetery is seen. "
                "(4) photo_on_grave_seen_indicator: TRUE or FALSE if a grave with an image is seen. "
                "(5) martyr_seen_indicator: TRUE or FALSE if the word martyr appears in any language. For example, in Arabic the word شهيدة means martyr. Additional words in Arabic might mean martyr."
            )

            response = generate_content_with_backoff(video_part, prompt)
            logging.info(f"Full response: {response.text}")

            # Parse the response text and extract description field
            try:
                response_json = json.loads(response.text)
                description = response_json[0][
                    'description'] if 'description' in response_json[
                    0] else "No description available."
            except (json.JSONDecodeError, KeyError, IndexError):
                logging.error(
                    "Failed to parse response. Extracting raw description.")
                description_lines = [line for line in response.text.split('\n')
                                     if 'description' in line]
                description = description_lines[0].split(':', 1)[
                    1].strip().strip(
                    '"') if description_lines else "No description available."

            cemetery_keywords = ['cemetery', 'grave', 'graveyard', 'tombstone']
            photo_keywords = ['photo', 'image', 'picture']
            martyr_keywords = ['شهيد', 'martyr']

            cemetery_seen_indicator = any(
                keyword in description.lower() for keyword in cemetery_keywords)
            photo_on_grave_seen_indicator = any(
                keyword in description.lower() for keyword in
                photo_keywords) and (
                                                        'tombstone' in description.lower() or 'grave' in description.lower())
            martyr_seen_indicator = any(
                keyword in description for keyword in martyr_keywords)

            record = {
                "file_name": blob.name,
                "description": description,
                "cemetery_seen_indicator": cemetery_seen_indicator,
                "photo_on_grave_seen_indicator": photo_on_grave_seen_indicator,
                "martyr_seen_indicator": martyr_seen_indicator
            }

            errors = bq_client.insert_rows_json(table_id, [record])
            if errors:
                logging.error(
                    f"Encountered errors while inserting row for {blob.name}: {errors}")
            else:
                logging.info(
                    f"Data for {blob.name} successfully inserted into BigQuery table.")

            request_count += 1
            logging.info(f"Processing completed for video: {blob.name}")
        except ResourceExhausted:
            logging.warning(
                f"Request limit exceeded for {blob.name}. Moving on to next video.")
        except Exception as e:
            logging.error(f"Error processing video {blob.name}: {e}")

logging.info("Processing completed for all videos.")
