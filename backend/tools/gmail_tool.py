import os.path
import base64
import markdown

from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar"
]


def gmail_authenticate():

    creds = None

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:

            token.write(creds.to_json())

    return creds


def send_email(to, subject, body):

    creds = gmail_authenticate()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    # Convert markdown → HTML
    html_body = markdown.markdown(body)

    # Beautiful email template
    styled_html = f"""
    <html>
    <body style="
        background-color:#0f172a;
        color:white;
        font-family:Arial,sans-serif;
        padding:40px;
    ">

        <div style="
            max-width:800px;
            margin:auto;
            background:#111827;
            border-radius:20px;
            padding:40px;
            border:1px solid #1f2937;
        ">

            <h1 style="
                color:#22d3ee;
                margin-bottom:30px;
            ">
                🚀 PilotOS AI Summary
            </h1>

            <div style="
                line-height:1.8;
                font-size:16px;
                color:#e5e7eb;
            ">
                {html_body}
            </div>

            <hr style="
                margin-top:40px;
                border:0;
                border-top:1px solid #374151;
            ">

            <p style="
                color:#9ca3af;
                margin-top:20px;
                font-size:14px;
            ">
                Generated autonomously by PilotOS
            </p>

        </div>

    </body>
    </html>
    """

    # Send HTML email
    message = MIMEText(
        styled_html,
        "html"
    )

    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    send_message = service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
    ).execute()

    return send_message