from app.agent.integration_agent import IntegrationAgent

def main():
    agent = IntegrationAgent()

    print("\nAI Integration Agent (MVP)")
    print("Describe the integration you want:\n")

    user_request = input("> ")

    workflow = agent.create_workflow(user_request)

    print("\nGenerated workflow:\n")
    print(workflow)

if __name__ == "__main__":
    main()
