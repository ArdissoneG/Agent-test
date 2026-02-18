class SlackTool:
    name = "Slack"

    def __init__(self, slack_client):
        self.slack = slack_client

    def run(self, action: dict):
        self.slack.send_message(
            channel=action["channel"],
            message=action["message"]
        )
