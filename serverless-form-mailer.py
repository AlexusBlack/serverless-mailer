import smtplib
import ssl
import json

account_file_path = 'smtp_account.json'

with open(account_file_path) as file:
  data = file.read()
  account = json.loads(data)

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(account['server'], account['port'], context=context) as server:
  server.login(account['user'], account['password'])
  # Send email here
  message = """\
Subject: Test message

Hi Alex from python script """
  server.sendmail(account['user'], 'alex@chernov.net', message)


