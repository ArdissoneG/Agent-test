class SheetsTool:
    name = "Google Sheets"

    def __init__(self, sheets_client):
        self.sheets = sheets_client

    def run(self, action: dict):
        values = action["values"]
        self.sheets.append_row(values)
