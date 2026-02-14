from app.agent.intent_parser import IntentParser


class WorkflowGenerator:
    def __init__(self):
        self.parser = IntentParser()

    def generate(self, user_request: str) -> dict:
        """
        Generates workflows based on parsed intent.
        Current support:
        - Google Forms → Google Sheets (+ optional Slack)
        """

        intent = self.parser.parse(user_request)

        # ---- Workflow 1: Google Forms ----
        if intent["trigger"] == "google_forms":

            actions = []

            if "google_sheets" in intent["actions"]:
                actions.append({
                    "app": "Google Sheets",
                    "event": "append_row",
                    "fields": ["name", "email", "message"]
                })

            if "slack" in intent["actions"]:
                actions.append({
                    "app": "Slack",
                    "event": "send_message",
                    "channel": "#notifications",
                    "message": "📩 New form submission received!"
                })

            return {
                "name": "Google Forms Automation",
                "trigger": {
                    "app": "Google Forms",
                    "event": "form_submitted"
                },
                "actions": actions
            }
        # ---- Workflow 2: Stripe Payment ----
        if intent["trigger"] == "stripe_payment":

            actions = []

            if "slack" in intent["actions"]:
                actions.append({
                    "app": "Slack",
                    "event": "send_message",
                    "channel": "#payments",
                    "message": "💰 New Stripe payment received!"
                })

            return {
                "name": "Stripe Payment Alert",
                "trigger": {
                    "app": "Stripe",
                    "event": "payment_succeeded"
                },
                "actions": actions
            }
        # ---- Fallback ----
        return {
            "error": "Workflow not supported yet",
            "supported": ["Google Forms → Sheets (+Slack)", "Stripe Payment → Slack"]
        }
