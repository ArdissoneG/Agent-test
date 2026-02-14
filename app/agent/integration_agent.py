from app.agent.workflow_generator import WorkflowGenerator
from app.storage.workflow_store import WorkflowStore
from app.integrations.slack import SlackIntegration
from app.utils.config import SLACK_WEBHOOK_URL


class IntegrationAgent:
    def __init__(self):
        self.generator = WorkflowGenerator()
        self.store = WorkflowStore()

        if SLACK_WEBHOOK_URL:
            self.slack = SlackIntegration()
        else:
            self.slack = None

    def create_workflow(self, user_request: str) -> dict:

        workflow = self.generator.generate(user_request)

        self.store.save(workflow)

        # Execute Slack action if present
        if self.slack:
            for action in workflow.get("actions", []):
                if action["app"] == "Slack":
                    self.slack.send_message(
                        channel=action["channel"],
                        message=action["message"]
                    )

        return workflow
