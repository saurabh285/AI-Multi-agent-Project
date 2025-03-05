from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def check_gmail():
    creds = None

    # Authenticate using credentials.json
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)


    # Connect to Gmail API
    service = build("gmail", "v1", credentials=creds)

    # Get unread emails
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get("messages", [])

    if not messages:
        print("✅ Gmail API is working, but no unread emails found.")
    else:
        print(f"✅ Gmail API is working! Found {len(messages)} unread emails.")

if __name__ == "__main__":
    check_gmail()
