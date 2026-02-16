import csv
import os


class MockGoogleSheetsIntegration:
    """
    Fake Google Sheets integration.
    Instead of writing to Google Sheets,
    it appends rows into a local CSV file.
    """

    def __init__(self, filepath="app/storage/sheets_mock.csv"):
        self.filepath = filepath

        # Create file with headers if it doesn't exist
        if not os.path.exists(self.filepath):
            with open(self.filepath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "email", "message"])

    def append_row(self, values: list):
        with open(self.filepath, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(values)

        print(f"✅ Row added to Mock Sheets CSV: {values}")
