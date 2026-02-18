from app.agent.workflow_generator import WorkflowGenerator
from app.storage.workflow_store import WorkflowStore

from app.integrations.slack import SlackIntegration
from app.integrations.mock_sheets import MockGoogleSheetsIntegration

from app.tools.sheets_tool import SheetsTool
from app.tools.slack_tool import SlackTool

from app.utils.config import SLACK_WEBHOOK_URL


class IntegrationAgent:
    def __init__(self):
        self.generator = WorkflowGenerator()
        self.store = WorkflowStore()

        # ----------------------------
        # Integrations (clients)
        # ----------------------------

        # Mock Google Sheets (local CSV)
        self.sheets = MockGoogleSheetsIntegration()

        # Slack integration (optional)
        if SLACK_WEBHOOK_URL:
            self.slack = SlackIntegration()
        else:
            self.slack = None

        # ----------------------------
        # Tools registry (NEW)
        # ----------------------------

        self.tools = {}

        # Register Sheets tool
        self.tools["Google Sheets"] = SheetsTool(self.sheets)

        # Register Slack tool only if available
        if self.slack:
            self.tools["Slack"] = SlackTool(self.slack)

    def create_workflow(self, user_request: str) -> dict:
        """
        Generates and saves a workflow JSON.
        Then executes supported actions.
        """

        workflow = self.generator.generate(user_request)

        # Save workflow
        self.store.save(workflow)

        # Execute actions
        self.execute_workflow(workflow)

        return workflow

    def execute_workflow(self, workflow: dict):
        """
        Executes each action using the correct tool.
        """

        for action in workflow.get("actions", []):

            tool = self.tools.get(action["app"])

            if tool:
                tool.run(action)
            else:
                print(f"⚠️ No tool registered for: {action['app']}")

