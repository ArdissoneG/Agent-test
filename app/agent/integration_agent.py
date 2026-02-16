from app.agent.workflow_generator import WorkflowGenerator
from app.storage.workflow_store import WorkflowStore

from app.integrations.slack import SlackIntegration
from app.integrations.mock_sheets import MockGoogleSheetsIntegration

from app.utils.config import SLACK_WEBHOOK_URL


class IntegrationAgent:
    def __init__(self):
        self.generator = WorkflowGenerator()
        self.store = WorkflowStore()

        # Mock Sheets integration (local CSV)
        self.sheets = MockGoogleSheetsIntegration()

        # Slack integration (optional)
        if SLACK_WEBHOOK_URL:
            self.slack = SlackIntegration()
        else:
            self.slack = None

    def create_workflow(self, user_request: str) -> dict:
        """
        Generates and saves a workflow JSON.
        Then executes supported actions.
        """

        workflow = self.generator.generate(user_request)

        # Save workflow
        self.store.save(workflow)

        # Execute actions dynamically
        self.execute_workflow(workflow)

        return workflow

    def execute_workflow(self, workflow: dict):
        """
        Executes each action in the workflow.
        """

        for action in workflow.get("actions", []):

            # Google Sheets (mock)
            if action["app"] == "Google Sheets":
                self.sheets.append_row(action["values"])

            # Slack
            if action["app"] == "Slack" and self.slack:
                self.slack.send_message(
                    channel=action["channel"],
                    message=action["message"]
                )
