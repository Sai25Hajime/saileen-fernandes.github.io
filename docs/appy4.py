from flask import Flask, request, redirect, render_template
import os
import base64
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

appy4 = Flask(__name__)

# Load credentials and create a Gmail API service
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CLIENT_SECRET_FILE = "client_secret.json"

service = None  # Fix: Do not authenticate on startup

def get_gmail_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, 
                SCOPES,
            )
            creds = flow.run_local_server(port=5001)  # Fix: Correct OAuth flow
            
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    return build("gmail", "v1", credentials=creds)

def send_email(name, sender_email, message_text):
    print(f"Debug: Sending email from {sender_email} with message: {message_text}")
    
    service = get_gmail_service()  # Fix: Authenticate only when needed
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

@appy4.route("/about")
def about():
    return render_template("about.html")

@appy4.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        sender_email = request.form["email"]
        message_text = request.form["message"]

        send_email(name, sender_email, message_text)

        return redirect("/")
    
    return render_template("contact.html")

@appy4.route("/test-email")
def test_email():
    send_email("Test User", "test@example.com", "This is a test email.")
    return "Test email sent!"

if __name__ == "__main__":
    appy4.run(debug=True, port=5001)
