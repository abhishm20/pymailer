import os
from pymailer import SECRET_FILE_PATH, GITHUB_LINK, CONF_PATH, SENDER_EMAIL_ID, send
import constants
import shutil


def setup():
    """
    Creates required directories 
    :return: 
    """
    if os.path.exists(CONF_PATH):
        shutil.rmtree(CONF_PATH)
    if not os.path.exists(SECRET_FILE_PATH):
        print '%sNo secret file found, please check %s%s'\
              % (constants.colors.ERROR, GITHUB_LINK, constants.colors.END)
        exit(-1)
    if not os.path.exists(CONF_PATH):
        print '%sCreating: %s%s' % (constants.colors.BOLD, CONF_PATH, constants.colors.END)
        os.makedirs(CONF_PATH)
    send(SENDER_EMAIL_ID, 'PyMailer :: setting up', 'Thank you for using PyMailer')


# Run setup whenever module is loaded
if __name__ == '__main__':
    setup()
