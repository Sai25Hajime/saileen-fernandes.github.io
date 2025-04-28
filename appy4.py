from flask import Flask, request, redirect, render_template
import os
import base64
import pickle
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

appy4 = Flask(__name__)

# Load credentials from environment variables (GitHub Secrets)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")

# OAuth 2.0 Configuration
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
REDIRECT_URI = "https://sai25hajime.github.io/saileen-fernandes.github.io/oauth2callback"  # Adjust if needed

service = None  # Do not authenticate on startup

def get_gmail_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                },
                SCOPES,
            )
            flow.redirect_uri = REDIRECT_URI
            creds = flow.run_local_server(port=5001)
        
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    return build("gmail", "v1", credentials=creds)

def send_email(name, sender_email, message_text):
    print(f"Debug: Sending email from {sender_email} with message: {message_text}")
    
    service = get_gmail_service()  # Authenticate only when needed
    if service is None:
        print("Error: Gmail API service is not initialized. Email not sent.")
        return

    try:
        message = MIMEText(f"Sender: {name}\nEmail: {sender_email}\n\nMessage:\n{message_text}")
        message["to"] = "saileenf6@gmail.com"  # Replace with your email
        message["subject"] = f"New Contact Form Submission from {name}"

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message}

        sent_message = service.users().messages().send(userId="me", body=body).execute()
        print("Debug: Email sent successfully!")
        return sent_message
    except Exception as e:
        print(f"Error sending email: {e}")

@appy4.route("/")
def index():
    return render_template("index.html")


@appy4.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        print("DEBUG: Contact form submitted!")  # Debugging
        name = request.form["name"]
        sender_email = request.form["email"]
        message_text = request.form["message"]

        send_email(name, sender_email, message_text)

        print(f"DEBUG: Email sent from {name} ({sender_email})")  # Debugging
        return redirect("/")
    
    return render_template("contact.html")

    
@appy4.route("/test-email")
def test_email():
    send_email("Test User", "test@example.com", "This is a test email.")
    return "Test email sent!"

if __name__ == "__main__":
    appy4.run(debug=True, port=5001)
