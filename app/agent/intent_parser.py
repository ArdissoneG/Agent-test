class IntentParser:
    """
    Simple rule-based parser for MVP.
    Later, this can be replaced with an LLM.
    """

    def parse(self, user_request: str) -> dict:
        text = user_request.lower()

        intent = {
            "trigger": None,
            "actions": []
        }

        # Detect trigger
        if "form" in text:
            intent["trigger"] = "google_forms"
            
        if "stripe" in text or "payment" in text:
            intent["trigger"] = "stripe_payment"

        # Detect actions
        if "sheet" in text or "spreadsheet" in text:
            intent["actions"].append("google_sheets")

        if "slack" in text or "notify" in text:
            intent["actions"].append("slack")

        return intent
