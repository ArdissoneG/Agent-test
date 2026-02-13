class WorkflowGenerator:
    def generate(self, user_request: str) -> dict:
        """
        Generates a basic workflow from the user request.
        MVP: Only supports Form → Google Sheets.
        """

        text = user_request.lower()

        if "form" in text and "sheet" in text:
            return {
                "name": "Form → Google Sheets",
                "trigger": {
                    "app": "Google Forms",
                    "event": "form_submitted"
                },
                "actions": [
                    {
                        "app": "Google Sheets",
                        "event": "append_row",
                        "fields": ["name", "email", "message"]
                    }
                ]
            }

        # Default fallback
        return {
            "error": "Workflow not supported yet in MVP",
            "supported": ["Form → Google Sheets"]
        }
