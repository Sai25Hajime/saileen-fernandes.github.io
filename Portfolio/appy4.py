from flask import Flask, request, redirect, render_template
import os
import base64
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

appy4 = Flask(__name__)

# Load credentials and create a Gmail API service
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CLIENT_SECRET_FILE = "client_secret.json"

def get_gmail_service():
    try:
       flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
       creds = flow.run_local_server(port=0)
       return build('gmail', 'v1', credentials=creds)
    except Exception as e:
       print(f"Error setting up Gmail service: {e}")
       return None

def send_email(name, sender_email, message_text):
    service = get_gmail_service()
    
    # Create email message
    message = MIMEText(f"Sender: {name}\nEmail: {sender_email}\n\nMessage:\n{message_text}")
    message["to"] = "your_email@gmail.com"  # Replace with your email
    message["subject"] = f"New Contact Form Submission from {name}"
    
    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw_message}

    # Send email using Gmail API
    message = service.users().messages().send(userId="me", body=body).execute()
    return message

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
    
    return render_template("contact.html")  # Show the contact form when accessed via GET


if __name__ == "__main__":
    appy4.run(debug=True)
