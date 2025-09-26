# Email_Calendar_Agent.py

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from langchain_google_community import CalendarToolkit
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.modify",
]

# ---------------- Google Auth ----------------
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
credentials = flow.run_local_server(port=0)

# Build Calendar API resource
calendar_api_resource = build("calendar", "v3", credentials=credentials)
calendar_toolkit = CalendarToolkit(api_resource=calendar_api_resource)

# Gmail toolkit (OAuth will reuse same token.json created above)
gmail_toolkit = GmailToolkit(credentials_path="credentials.json")

print("✅ Gmail tools loaded:", gmail_toolkit.get_tools())
print("✅ Calendar tools loaded:", calendar_toolkit.get_tools())

# ---------------- LLM Setup ----------------

llm = init_chat_model("google_genai:gemini-2.5-flash", api_key="AIzaSyDSFL3U4sdcDvNdeUwuH2aWgqzLrEeB9Ck", temperature=0.0)

# ---------------- Specialist Agents ----------------
email_agent = create_react_agent(
    model=llm,
    tools=gmail_toolkit.get_tools(),
    name="email_agent",
    prompt="""
    You are an expert Gmail assistant. Your role is to manage and automate emails.
    Always use the provided Gmail tools to:
    - Draft and send emails
    - Search for existing messages or threads
    - Fetch message content if needed
    
    Guidelines:
    - Never ask the user to repeat information you can infer.
    - If the user requests an invitation or meeting notice, assume the calendar_agent will create the event first. 
    - After the event is created, send a confirmation/invitation email using GmailSendMessage.
    - Be proactive: use the context provided to fill in subject and body lines (e.g., "Interview Invitation - {date/time}").
    """
)

calendar_agent = create_react_agent(
    model=llm,
    tools=calendar_toolkit.get_tools(),
    name="calendar_agent",
    prompt="""
    You are an expert Google Calendar assistant. 
    Your job is to create, search, update, and manage events using the provided Calendar tools.
    
    Guidelines:
    - Always interpret natural language times (e.g., "tomorrow at 3pm IST") into exact datetime values. 
    - Use the GetCurrentDatetime tool if you need the current date to resolve "tomorrow", "next week", etc.
    - When creating events, include:
      • Title (e.g., "Interview with Candidate")  
      • Start & End times (default 1 hour if not specified)  
      • Attendees (emails mentioned in the request)  
      • Description if relevant  
    
    - Never ask the user to repeat details unless absolutely missing.
    - After scheduling, summarize the event details clearly.
    - If the task also involves notifying attendees → transfer control to email_agent to send the invitation.
    """

)

# ---------------- Supervisor ----------------
supervisor = create_supervisor(
    [email_agent, calendar_agent],
    model=llm,
    prompt="""
    You are a supervisor managing multiple specialist agents. 
    Your job is to route tasks to the correct agent:

    - Use **calendar_agent** for all tasks related to scheduling, creating, updating, or managing events.
    - Use **email_agent** for tasks related to sending, drafting, or searching emails.
    - If a task requires both scheduling and sending an email (e.g., "invite someone to a meeting"), 
      first call the calendar_agent to create the event, then transfer to email_agent to send the invitation.

    Never perform the task yourself; always delegate to the correct agent.
    """
)

app = supervisor.compile()

# ---------------- Memory + Store ----------------
# checkpointer = InMemorySaver()
# store = InMemoryStore()

if __name__=="__main__":

    # ---------------- Test ----------------
    result = app.invoke({
        "messages": [
            {"role": "user", "content": "Invite sarath.bandreddi@commdel.net that he is selected for the interview tomorrow at 3pm IST."}
        ]
    })

    for m in result["messages"]:
        m.pretty_print()

