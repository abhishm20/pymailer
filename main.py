import sys
import pymailer
import os
from pymailer import CONF_PATH, CURRENT_DIR
import constants


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
    while argv: # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts


if __name__ == '__main__':
    if not os.path.exists(CONF_PATH) or not os.path.exists(CURRENT_DIR):
        print '%sPlease run setup...%s' % (constants.colors.ERROR, constants.colors.END)
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
        print "%sError: %s%s" % (constants.colors.ERROR, str(e), constants.colors.END)
        exit()

    # pymailer.send('abhishek.sharma@daybox.in', 'hello', 'body')
    pymailer.send(email, subject, body)
