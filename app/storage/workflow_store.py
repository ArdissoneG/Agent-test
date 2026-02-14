import json
import os
from datetime import datetime


class WorkflowStore:
    def __init__(self, folder: str = "app/workflows"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def save(self, workflow: dict):
        """
        Saves the workflow into a JSON file with timestamp.
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workflow_{timestamp}.json"
        path = os.path.join(self.folder, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=4)

        print(f"\n✅ Workflow saved to: {path}")
