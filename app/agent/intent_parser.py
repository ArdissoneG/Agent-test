import re


class IntentParser:
    """
    Very simple NLP parser for MVP.
    Extracts:
    - trigger
    - actions
    - optional user data for Sheets
    """

    def parse(self, text: str) -> dict:

        intent = {
            "trigger": None,
            "actions": [],
            "data": {}
        }

        lower = text.lower()

        # ----------------------------
        # Detect trigger
        # ----------------------------
        if "form" in lower:
            intent["trigger"] = "google_forms"

        if "stripe" in lower or "payment" in lower:
            intent["trigger"] = "stripe_payment"

        # Default trigger if unknown
        if intent["trigger"] is None:
            intent["trigger"] = "manual"

        # ----------------------------
        # Detect actions
        # ----------------------------
        if "sheet" in lower or "spreadsheet" in lower:
            intent["actions"].append("google_sheets")

        if "slack" in lower or "notify" in lower:
            intent["actions"].append("slack")

        # ----------------------------
        # Extract structured data
        # Format:
        # Add to sheet: name,email,message
        # ----------------------------
        match = re.search(r"add to sheet:\s*(.*)", text, re.IGNORECASE)

        if match:
            parts = match.group(1).split(",")

            if len(parts) >= 3:
                intent["data"] = {
                    "name": parts[0].strip(),
                    "email": parts[1].strip(),
                    "message": parts[2].strip()
                }

        return intent
