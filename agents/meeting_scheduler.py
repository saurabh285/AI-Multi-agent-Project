import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def authenticate_google_calendar():
    """Authenticate and return a Google Calendar API service instance."""
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("calendar", "v3", credentials=creds)

def get_upcoming_events(service, date, max_results=5):
    """Fetch events from Google Calendar for a specific date."""
    start_of_day = f"{date}T00:00:00Z"
    end_of_day = f"{date}T23:59:59Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_of_day,
        timeMax=end_of_day,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events_result.get("items", [])

def suggest_meeting_times(service):
    """Find the next available meeting slot starting from today."""
    days_checked = 0
    max_days_ahead = 7  # Look up to a week ahead for free slots

    while days_checked < max_days_ahead:
        # Get the date for the day we are checking
        date_to_check = (datetime.datetime.utcnow() + datetime.timedelta(days=days_checked)).strftime("%Y-%m-%d")

        # Get events for that day
        events = get_upcoming_events(service, date_to_check)

        # Get busy times from events
        busy_times = []
        for event in events:
            start_time = event["start"].get("dateTime", event["start"].get("date"))
            end_time = event["end"].get("dateTime", event["end"].get("date"))
            busy_times.append((start_time, end_time))

        # Define work hours (9 AM - 6 PM)
        available_slots = []
        work_hours = [(f"0{h}:00:00" if h < 10 else f"{h}:00:00") for h in range(9, 18)]

        # Check for free slots within work hours
        for i in range(len(work_hours) - 1):
            slot_start = f"{date_to_check}T{work_hours[i]}Z"
            slot_end = f"{date_to_check}T{work_hours[i+1]}Z"
            
            if not any(start <= slot_start <= end for start, end in busy_times):
                available_slots.append(f"{date_to_check} {work_hours[i]} - {work_hours[i+1]}")

        if available_slots:
            return available_slots  # Return slots as soon as we find availability

        # Move to the next day if no slots available today
        days_checked += 1

    return ["No available slots in the next 7 days."]

def save_meeting_suggestions(slots, filename="meeting_suggestions.txt"):
    """Save meeting suggestions to a file (overwrite if exists)."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("⏳ **Suggested Meeting Slots:**\n")
        for slot in slots:
            file.write(f"✅ {slot}\n")

if __name__ == "__main__":
    calendar_service = authenticate_google_calendar()
    available_slots = suggest_meeting_times(calendar_service)

    save_meeting_suggestions(available_slots)

    print("\n✅ Meeting suggestions saved to 'meeting_suggestions.txt'!")
