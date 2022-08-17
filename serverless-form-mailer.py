import smtplib
import ssl
# import json
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

account = config['SMTP Account']
settings = config['Settings']

allowed_origins = settings['Allowed Origins'].strip().split("\n")
print(allowed_origins)
quit()

# def lambda_handler(event, context):
#   allowed_origins = ['http://localhost:3000', 'https://redsuburbs.com.au']
#   origin = event['headers']['origin'] if 'origin' in event['headers'] else None
#
#   if origin != None and origin not in allowed_origins:
#     return {
#       'statusCode': 403,
#       'body': json.dumps('You are not allowed to access this resource')
#     }

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(account['Server'], account['Port'], context=context) as server:
  server.login(account['User'], account['Password'])
  # Send email here
  message = """\
Subject: Test message 2

Hi Alex from python script 2"""
  server.sendmail(account['user'], 'alex@chernov.net', message)


