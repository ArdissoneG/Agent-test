import os
import requests
from dotenv import load_dotenv

load_dotenv()


class SlackIntegration:
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

        if not self.webhook_url:
            raise ValueError("Missing SLACK_WEBHOOK_URL in .env")

    def send_message(self, channel: str, message: str):
        payload = {
            "text": message
        }

        response = requests.post(self.webhook_url, json=payload)

        if response.status_code != 200:
            raise Exception(
                f"Slack error: {response.status_code}, {response.text}"
            )

        print("✅ Slack message sent successfully!")
