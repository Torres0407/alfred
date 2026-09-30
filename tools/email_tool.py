import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly"
]

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")


def _get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_email(to: str, subject: str, body: str) -> str:
    try:
        service = _get_gmail_service()

        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return f"Email sent to {to} with subject '{subject}'."
    except Exception as e:
        return f"Couldn't send email: {e}"

def list_recent_emails(max_results: int = 10, query: str = "") -> str:
    try:
        service = _get_gmail_service()
        results = service.users().messages().list(
            userId="me", maxResults=max_results, q=query
        ).execute()
        messages = results.get("messages", [])

        if not messages:
            return "No emails found."

        lines = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId="me", id=msg["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]
            ).execute()
            headers = {h["name"]: h["value"] for h in msg_data["payload"]["headers"]}
            snippet = msg_data.get("snippet", "")
            lines.append(
                f"[{msg['id']}] From: {headers.get('From', '?')} | "
                f"Subject: {headers.get('Subject', '(no subject)')} | "
                f"Date: {headers.get('Date', '?')}\nPreview: {snippet}\n"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Couldn't list emails: {e}"


def read_email(email_id: str) -> str:
    try:
        service = _get_gmail_service()
        msg = service.users().messages().get(userId="me", id=email_id, format="full").execute()

        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        subject = headers.get("Subject", "(no subject)")
        sender = headers.get("From", "?")

        body = ""
        payload = msg["payload"]
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                    break
        elif "data" in payload.get("body", {}):
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")

        if len(body) > 4000:
            body = body[:4000] + "\n...[truncated]"

        return f"From: {sender}\nSubject: {subject}\n\n{body or '(no readable text content)'}"
    except Exception as e:
        return f"Couldn't read email: {e}"