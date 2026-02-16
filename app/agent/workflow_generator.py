from app.agent.intent_parser import IntentParser


class WorkflowGenerator:
    def __init__(self):
        self.parser = IntentParser()

    def generate(self, user_request: str) -> dict:
        """
        Generates workflows based on parsed intent.
        Current support:
        - Google Forms → Google Sheets (+ optional Slack)
        - Stripe Payment → Slack
        """

        intent = self.parser.parse(user_request)

        actions = []

        # ----------------------------
        # Google Sheets Action
        # ----------------------------
        if "google_sheets" in intent["actions"]:

            data = intent.get("data", {})

            actions.append({
                "app": "Google Sheets",
                "event": "append_row",
                "fields": ["name", "email", "message"],
                "values": [
                    data.get("name", "unknown"),
                    data.get("email", "unknown"),
                    data.get("message", "empty")
                ]
            })

        # ----------------------------
        # Slack Action
        # ----------------------------
        if "slack" in intent["actions"]:

            channel = "#notifications"

            if intent["trigger"] == "stripe_payment":
                msg = "💰 New Stripe payment received!"
                channel = "#payments"
            else:
                msg = "📩 New workflow event triggered!"

            actions.append({
                "app": "Slack",
                "event": "send_message",
                "channel": channel,
                "message": msg
            })

        # ----------------------------
        # Workflow Output
        # ----------------------------
        return {
            "name": f"{intent['trigger']} automation",
            "trigger": {
                "app": intent["trigger"],
                "event": "triggered"
            },
            "actions": actions
        }
