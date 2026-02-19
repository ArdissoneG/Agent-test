import inspect
import pkgutil
import importlib

import app.tools as tools_package
from app.tools.base import Tool

from app.agent.workflow_generator import WorkflowGenerator
from app.storage.workflow_store import WorkflowStore

from app.integrations.slack import SlackIntegration
from app.integrations.mock_sheets import MockGoogleSheetsIntegration

from app.utils.config import SLACK_WEBHOOK_URL

from app.agent.decision_maker import DecisionMaker


class IntegrationAgent:
    def __init__(self):
        self.generator = WorkflowGenerator()
        self.store = WorkflowStore()
        self.decision_maker = DecisionMaker()

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
        # Tool Auto-Discovery
        # ----------------------------

        self.tools = {}

        # Dynamically import all modules inside app.tools
        for _, module_name, _ in pkgutil.iter_modules(tools_package.__path__):
            module = importlib.import_module(f"app.tools.{module_name}")

            for _, cls in inspect.getmembers(module, inspect.isclass):

                if issubclass(cls, Tool) and cls is not Tool:

                    # Dependency injection based on tool name
                    if cls.name == "Google Sheets":
                        instance = cls(self.sheets)

                    elif cls.name == "Slack" and self.slack:
                        instance = cls(self.slack)

                    else:
                        continue

                    self.tools[cls.name] = instance

    def create_workflow(self, user_request: str) -> dict:
        """
        Classifies user intent.
        Only generates workflow if automation intent detected.
        """

        decision = self.decision_maker.classify(user_request)

        if decision != "automation":
            print("No automation detected. Ignoring input.")
            return {"status": "ignored"}

        workflow = self.generator.generate(user_request)

        self.store.save(workflow)
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


