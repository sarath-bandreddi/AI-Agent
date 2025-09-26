# Email_Calendar_Agent.py
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_google_community import CalendarToolkit
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
from langchain.agents import initialize_agent, AgentType

def main():
    SCOPES = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/gmail.modify",
    ]

    # ---------------- Google Auth ----------------# Email_Calendar_Agent.py
    # from google_auth_oauthlib.flow import InstalledAppFlow
    # from googleapiclient.discovery import build
    # from langchain_google_community import CalendarToolkit
    # from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
    # from langchain.agents import initialize_agent, AgentType
    #
    # def main():
    #     SCOPES = [
    #         "https://www.googleapis.com/auth/calendar",
    #         "https://www.googleapis.com/auth/gmail.modify",
    #     ]
    #
    #     # ---------------- Google Auth ----------------
    #     # OAuth login flow using same credentials.json for both Gmail + Calendar
    #     flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    #     credentials = flow.run_local_server(port=0)
    #
    #     # Build Calendar API resource
    #     calendar_api_resource = build("calendar", "v3", credentials=credentials)
    #     calendar_toolkit = CalendarToolkit(api_resource=calendar_api_resource)
    #
    #     # Gmail toolkit (OAuth will reuse same token.json created above)
    #     gmail_toolkit = GmailToolkit(credentials_path="credentials.json")
    #
    #     print("✅ Gmail tools loaded:", gmail_toolkit.get_tools())
    #     print("✅ Calendar tools loaded:", calendar_toolkit.get_tools())
    #
    #
    #     # ---------------- Unified Agent ----------------
    #     agent = initialize_agent(
    #         tools=gmail_toolkit.get_tools() + calendar_toolkit.get_tools(),
    #         llm=llm,
    #         agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    #         verbose=True,
    #     )
    #
    #     # ---------------- Test ----------------
    #     # result1 = agent.invoke("Create a new calendar event tomorrow at 3pm titled 'Project Review Meeting'")
    #     # print("\n📅 Calendar Response:", result1["output"])
    #     #
    #     # result2 = agent.invoke("Draft an email to my team reminding them about the 'Project Review Meeting' tomorrow at 3pm.")
    #     # print("\n📧 Gmail Response:", result2["output"])
    #
    #     result3 = agent.invoke("Invite prabhakarrel@gmail.com that he selected for the interview tomorrow at 3pm.")
    #     print("\n📧 Gmail Invite Response:", result3["output"])
    #
    # if __name__ == "__main__":
    #     main()
    # OAuth login flow using same credentials.json for both Gmail + Calendar
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    credentials = flow.run_local_server(port=0)

    # Build Calendar API resource
    calendar_api_resource = build("calendar", "v3", credentials=credentials)
    calendar_toolkit = CalendarToolkit(api_resource=calendar_api_resource)

    # Gmail toolkit (OAuth will reuse same token.json created above)
    gmail_toolkit = GmailToolkit(credentials_path="credentials.json")

    print("✅ Gmail tools loaded:", gmail_toolkit.get_tools())
    print("✅ Calendar tools loaded:", calendar_toolkit.get_tools())

    llm = None

    # ---------------- Unified Agent ----------------
    agent = initialize_agent(
        tools=gmail_toolkit.get_tools() + calendar_toolkit.get_tools(),
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # ---------------- Test ----------------
    # result1 = agent.invoke("Create a new calendar event tomorrow at 3pm titled 'Project Review Meeting'")
    # print("\n📅 Calendar Response:", result1["output"])
    #
    # result2 = agent.invoke("Draft an email to my team reminding them about the 'Project Review Meeting' tomorrow at 3pm.")
    # print("\n📧 Gmail Response:", result2["output"])

    result3 = agent.invoke("Invite sarath.bandreddi@commdel.net that he selected for the interview tomorrow at 3pm.")
    print("\n📧 Gmail Invite Response:", result3["output"])

if __name__ == "__main__":
    main()