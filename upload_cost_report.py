from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Use environment variables for security
# Set these before running:
#   export SLACK_TOKEN="xoxb-your-token"
#   export SLACK_CHANNEL="C08XXXXXXXX"

slack_token = os.environ.get("SLACK_TOKEN", "xoxb-your-token-here")
channel_id = os.environ.get("SLACK_CHANNEL", "C08XXXXXXXX")

client = WebClient(token=slack_token)

try:
    # Use files_upload_v2 (latest method)
    response = client.files_upload_v2(
        channel=channel_id,
        initial_comment="AWS Cost Report",
        file="cost-report.txt"
    )
    print("File uploaded successfully!")
except SlackApiError as e:
    print(f"Error uploading file: {e.response['error']}")
