import openai
from app.utils.config import OPENAI_API_KEY


class DecisionMaker:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def classify(self, user_input: str) -> str:
        """
        Returns:
        - 'automation'
        - 'ignore'
        """

        prompt = f"""
You are an automation intent classifier.

Classify the following user input into one of these categories:
- automation
- ignore

Only return one word.

User input:
{user_input}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response["choices"][0]["message"]["content"].strip().lower()

        return result
