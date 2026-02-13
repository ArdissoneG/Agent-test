from app.agent.workflow_generator import WorkflowGenerator
from app.storage.workflow_store import WorkflowStore


class IntegrationAgent:
    def __init__(self):
        self.generator = WorkflowGenerator()
        self.store = WorkflowStore()

    def create_workflow(self, user_request: str) -> dict:
        """
        Takes a natural language request and returns a workflow dict.
        Also saves it to the workflows/ folder.
        """

        workflow = self.generator.generate(user_request)

        # Save workflow as JSON file
        self.store.save(workflow)

        return workflow
