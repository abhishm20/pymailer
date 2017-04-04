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
1. goto **downloads** directory where pymailer is downloaded
```bash
# e.g. cd ~/Downloads/
```
2. move **pymailer** to **home** directory
```bash
mv -R pymailer ~/
```
2. set **pymailer** as variable
```bash
printf "export PYMAILER=\"~/home/pymailer/pymailer.py\"" >> ~/.bash_profile
```
4. set **alias** to execute as command
```bash
printf "alias pymailer='python \$PYMAILER'" >> ~/.bash_profile
```
5. load changes
```bash
source ~/.bash_profile
```
6. test sending a mail
```bash
pymailer -e test@gmail.com -s subject -b body
```
