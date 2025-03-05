from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def check_calendar():
    creds = None

    # Authenticate using credentials.json
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Connect to Google Calendar API
    service = build("calendar", "v3", credentials=creds)

    # Get upcoming events
    events_result = service.events().list(calendarId="primary", maxResults=5, singleEvents=True, orderBy="startTime").execute()
    events = events_result.get("items", [])

    if not events:
        print("✅ Google Calendar API is working, but no upcoming events found.")
    else:
        print("✅ Google Calendar API is working! Here are the next events:")
        for event in events:
            print(f"- {event['summary']} at {event['start'].get('dateTime', event['start'].get('date'))}")

if __name__ == "__main__":
    check_calendar()
