from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

import random
import email
import subprocess


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          "https://www.googleapis.com/auth/gmail.send"]


def CreateMessage(sender, to, subject, cc, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message["cc"] = cc
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def handel_inputs(email_contents,to,subject, cc, day, time):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    msg = CreateMessage(
        "me", to,subject,cc,email_contents)
    message = service.users().messages().send(userId='me', body=msg).execute()

    save_data = {
        "email_contents" : email_contents,
        "to" : to,
        "subject": subject,
        "cc": cc,
        "day": day,
        "time": time,
    }
    os.system("powershell Unregister-ScheduledTask -TaskName EmailTask -Confirm:$false")
    os.system("start chrome.exe gmail.com youtube.com facebook.com")
    command = 'powershell $Sta = New-ScheduledTaskAction -Execute "email_automizer.exe" -WorkingDirectory "{0}"; $STSet = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries; $Stt = New-ScheduledTaskTrigger -Weekly -WeeksInterval 1 -DaysOfWeek {1} -At {2};Register-ScheduledTask EmailTask -Action $Sta -Trigger $Stt -Settings $STSet;'.format(os.path.realpath('...'),day,time)
    os.system(command)
    with open("saved_data.pickle","wb+") as f:
        pickle.dump(save_data,f)