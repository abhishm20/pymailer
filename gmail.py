import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import constants

import httplib2
import oauth2client
from apiclient import errors, discovery
from oauth2client import client, tools

APPLICATION_NAME = 'pygmailer'

# Internal constant
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

# Home directory
HOME_DIR = os.path.expanduser('~')

# Configuration path (HOME/.pymailer)
CONF_PATH = os.path.join(HOME_DIR, '.'+APPLICATION_NAME)
# Credential path (HOME/.pymailer/.credentials)
CREDENTIAL_PATH = os.path.join(HOME_DIR, '.'+APPLICATION_NAME, '.credentials')

CREDENTIAL_FILE_NAME = 'oauth2.json'
SECRET_FILE_NAME = "client_secret.json"

SECRET_FILE_PATH = os.path.join(CONF_PATH, SECRET_FILE_NAME)

SENDER_EMAIL_ID = 'contact@daybox.in'


def setup():
    """
    Creates required directories 
    :return: 
    """
    if not os.path.exists(CONF_PATH):
        print '%Creating %s%s' % (constants.colors.BOLD, CONF_PATH, constants.colors.END)
        os.makedirs(CONF_PATH)
    if not os.path.exists(CREDENTIAL_PATH):
        print '%Creating %s%s' % (constants.colors.BOLD, CREDENTIAL_PATH, constants.colors.END)
        os.makedirs(CREDENTIAL_PATH)
    if not os.path.exists(SECRET_FILE_PATH):
        print '%sNo secret file found, please check %s' % (constants.colors.ERROR, constants.colors.END)
        exit(-1)


def _get_credentials():
    credential_path = os.path.join(CREDENTIAL_PATH, CREDENTIAL_FILE_NAME)
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(SECRET_FILE_PATH, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print '%sStoring credentials to %s%s' % (constants.colors.BOLD, credential_path, constants.colors.END)
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
        print '%sSuccessfully sent%s' % (constants.colors.SUCCESS, constants.colors.END)
        print '%smail message id: %s%s' % (constants.colors.BOLD, message['id'], constants.colors.END)
        return message['id']
    except errors.HttpError, error:
        print '%serror: %s%s' % (constants.colors.ERROR, error, constants.colors.END)


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
    print "%smail-data: %s %s%s" % (constants.colors.BLUE, email, subject, constants.colors.END)
    _send_email(email, subject, body)


# Run setup whenever module is loaded
setup()
