import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
