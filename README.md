# pymailer
A python utility to send mail from gmail using OAuth2.0


### Required libs
1. to install **httplib2**
```bash
pip install --upgrade httplib2
```
2. to install **oauth2client**
```bash
pip install --upgrade oauth2client
```
3. to install **google-api-python-client**
```bash
pip install --upgrade google-api-python-client
```

### Setup
1. goto **pymailer** directory

2. run **setup**
```bash
python setup.py
```

### To send email
1. goto **pymailer** directory

2. send **email**
```bash
python main.py -e test@gmail.com -s subject -b body
```