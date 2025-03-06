import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import google.generativeai as genai  # Gemini API

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Authenticate Gemini API
genai.configure(api_key=GEMINI_API_KEY)

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """Authenticate and return a Gmail API service instance."""
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

def get_unread_emails(service, max_results=5):
    """Fetch unread emails from Gmail."""
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread", maxResults=max_results).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        subject = next((header["value"] for header in msg_data["payload"].get("headers", []) if header["name"] == "Subject"), "No Subject")
        snippet = msg_data.get("snippet", "")
        emails.append({"subject": subject, "snippet": snippet})

    return emails

def summarize_emails(emails):
    """Use Gemini API to summarize emails."""
    if not emails:
        return "No new unread emails."

    email_text = "\n\n".join([f"Subject: {email['subject']}\nSnippet: {email['snippet']}" for email in emails])

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Summarize these emails briefly:\n{email_text}")

    return response.text if response else "Failed to generate summary."

def generate_smart_replies(email):
    """Generate clean, professional smart reply suggestions for an email."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Generate three short, polite, and professional reply suggestions for the following email.\n"
        "DO NOT number or format the replies, and avoid empty lines.\n\n"
        f"Subject: {email['subject']}\nSnippet: {email['snippet']}"
    )
    response = model.generate_content(prompt)

    if response and response.text:
        # Cleanly parse replies, ignoring empty lines
        replies = [line.strip().strip('"').strip("'") for line in response.text.split("\n") if line.strip()]
        # Limit to exactly three replies
        return replies[:3] if replies else ["No reply suggestions available."]
    return ["No reply suggestions available."]


def save_to_file(emails, summary, filename="email_summaries.txt"):
    """Save email summaries and smart replies to a file (overwrite if exists)."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("📩 **Unread Emails:**\n")
        for email in emails:
            file.write(f"- {email['subject']}: {email['snippet']}\n")
        
        file.write("\n📝 **Email Summary:**\n")
        file.write(summary + "\n")

        file.write("\n💬 **Smart Reply Suggestions:**\n")
        for email in emails:
            replies = generate_smart_replies(email)
            file.write(f"\n📧 Subject: {email['subject']}\n")
            for i, reply in enumerate(replies, start=1):
                file.write(f"🔹 Reply {i}: {reply}\n")

if __name__ == "__main__":
    gmail_service = authenticate_gmail()
    unread_emails = get_unread_emails(gmail_service, max_results=3)

    summary = summarize_emails(unread_emails)

    save_to_file(unread_emails, summary)

    print("\n✅ Email summaries and smart replies saved to 'email_summaries.txt'!")
