from google.cloud import pubsub_v1

# Replace these with your own values
project_id = "your_project_id"
topic_id = "your_topic_id"

# Initialize the publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def callback(future):
    message_id = future.result()
    print(f"Message published with ID: {message_id}")

# The data that you want to send
data = "Hello, World!"
data = data.encode("utf-8")

# Publish the message
future = publisher.publish(topic_path, data=data)
future.add_done_callback(callback)

# Keep the script alive until the message is sent
future.result()
