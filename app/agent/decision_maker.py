import requests


class DecisionMaker:
    def __init__(self, model: str = "phi3:mini"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

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

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            print("Ollama error:", response.text)
            return "ignore"

        result = response.json()["response"].strip().lower()

        if "automation" in result:
            return "automation"

        return "ignore"