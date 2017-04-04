#!/usr/bin/env python
import argparse
import base64
import os
import shutil
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httplib2
import oauth2client
from apiclient import errors, discovery
from oauth2client import client, tools

APPLICATION_NAME = 'pymailer'

# Internal constant
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

# Home directory
HOME_DIR = os.path.expanduser('~')

# Current directory
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Configuration path (HOME/.pymailer)
CONF_PATH = os.path.join(HOME_DIR, '.' + APPLICATION_NAME)

CREDENTIAL_FILE_NAME = 'credentials.json'
SECRET_FILE_NAME = "client_secret.json"

SECRET_FILE_PATH = os.path.join(CURRENT_DIR, SECRET_FILE_NAME)
CREDENTIAL_FILE_PATH = os.path.join(CONF_PATH, CREDENTIAL_FILE_NAME)

SENDER_EMAIL_ID = 'pymailertool@gmail.im'

# Github link
GITHUB_LINK = "https://github.com/abhishm20/pymailer"


# colors
class colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _get_credentials():
    store = oauth2client.file.Storage(CREDENTIAL_FILE_PATH)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(SECRET_FILE_PATH, SCOPES)
        flow.user_agent = APPLICATION_NAME
        parser = argparse.ArgumentParser()
        parser.add_argument("--noauth_local_webserver", default=True)
        parser.add_argument("--logging_level", default='ERROR')
        parser.add_argument("--auth_host_name", default='localhost')
        parser.add_argument("--auth_host_port", default=[8080, 8090])
        flags = parser.parse_args()
        credentials = tools.run_flow(flow, store, flags=flags)
        print '%sStoring credentials to %s%s' % (colors.BOLD, CREDENTIAL_FILE_PATH, colors.END)
    return credentials


def _send_message(sender, to, subject, msgHtml, msgPlain):
    credentials = _get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = _create_message(sender, to, subject, msgHtml, msgPlain)
    return _send_message_internal(service, "me", message1)


def _send_message_internal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print '%sSuccessfully sent%s' % (colors.SUCCESS, colors.END)
        print '%smail message id: %s%s' % (colors.BOLD, message['id'], colors.END)
        return message['id']
    except errors.HttpError, error:
        print '%serror: %s%s' % (colors.ERROR, error, colors.END)


def _create_message(sender, to, subject, msg_html, msg_plain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msg_plain, 'plain'))
    msg.attach(MIMEText(msg_html, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string())}


def _send_email(email, subject, body):
    to = email
    sender = SENDER_EMAIL_ID
    subject = subject
    msg_html = body
    return _send_message(sender, to, subject, msg_html, '')


def send(email, subject, body):
    print "%smail-data: %s %s%s" % (colors.BLUE, email, subject, colors.END)
    _send_email(email, subject, body)


# Validation error class
class ValidationError(Exception):
    def __init__(self, message, errors=[]):
        # Call the base class constructor with the parameters it needs
        super(ValidationError, self).__init__(message)
        # Now for your custom code...
        self.errors = errors


# Command line arguments interpreter
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts


def setup():
    """
    Creates required directories 
    :return: 
    """
    if os.path.exists(CONF_PATH):
        shutil.rmtree(CONF_PATH)
    if not os.path.exists(SECRET_FILE_PATH):
        print '%sNo secret file found, please check %s%s' \
              % (colors.ERROR, GITHUB_LINK, colors.END)
        exit(-1)
    if not os.path.exists(CONF_PATH):
        print '%sCreating: %s%s' % (colors.BOLD, CONF_PATH, colors.END)
        os.makedirs(CONF_PATH)
    send(SENDER_EMAIL_ID, 'PyMailer :: setting up', 'Thank you for using PyMailer')


if __name__ == '__main__':
    if not os.path.exists(CONF_PATH) or not os.path.exists(CURRENT_DIR):
        print '%sPlease run setup...%s' % (colors.ERROR, colors.END)
        exit(-1)

    myargs = getopts(sys.argv)
    email = ''
    subject = ''
    body = ''
    try:
        if '-e' in myargs:  # Example usage.
            email = myargs['-e']
        else:
            raise ValidationError("email id is required")

        if '-s' in myargs:  # Example usage.
            subject = myargs['-s']
        else:
            raise ValidationError("mail subject is required")

        if '-b' in myargs:  # Example usage.
            body = myargs['-b']
        else:
            raise ValidationError("mail body is required")
    except Exception as e:
        print "%sError: %s%s" % (colors.ERROR, str(e), colors.END)
        exit()

    send(email, subject, body)
