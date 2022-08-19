import smtplib
import ssl
import json
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

account = config['SMTP Account']
settings = config['Settings']

allowed_origins = settings['Allowed Origins'].strip().split("\n")
allowed_emails = settings['Allowed Destination Emails'].strip().split("\n")

# AWS compatible handler
def lambda_handler(event, context):
  return the_lambda_handler(event, context)

# Use this for testing, pass dry run
def the_lambda_handler(event, context, dry_run = False):
  request_format_error = find_request_format_error(event)
  if request_format_error != None: return request_format_error

  if is_options_request(event):
    return {
      'statusCode': 200,
      'headers': {
        'Access-Control-Allow-Origin': event['headers']['origin'],
        'Access-Control-Allow-Headers': '*',
        'Allow': 'OPTIONS, POST'
      },
      'body': ''
    }

  is_error, data = parse_request_data(event)
  if is_error: return data

  if not dry_run:
    send_email(account, data['to_email'], data['subject'], data['content'])

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Origin': event['headers']['origin']
      },
    'body': json.dumps('Email sent')
  }

def parse_request_data(event):
  try:
    data = json.loads(event['body'])
  except json.JSONDecodeError:
    return True, {
      'statusCode': 400,
      'body': json.dumps('Request body is not a valid JSON')
    }

  if 'subject' not in data or 'content' not in data:
    return True, {
      'statusCode': 400,
      'body': json.dumps('Request body missing subject or content')
    }

  # Identify recipient of the email
  if 'to' in data:
    if data['to'] not in allowed_emails:
      return True, {
        'statusCode': 400,
        'body': json.dumps('The recipient is not allowed')
      }
    else:
      to_email = data['to']
  else:
    to_email = settings['Default Destination Email'].strip()

  return False, {
    'to_email': to_email,
    'subject': data['subject'],
    'content': data['content']
  }

def find_request_format_error(event):
  if not is_allowed_origin(event):
    return {
      'statusCode': 403,
      'body': json.dumps('You are not allowed to access this resource')
    }

  if event['requestContext']['http']['method'] not in ['POST', 'OPTIONS']:
    return {
      'statusCode': 405,
      'body': json.dumps('This http method is not allowed.')
    }

  # No need to check for body in options request
  if is_options_request(event): return None

  if 'body' not in event or event['body'] is None:
    return {
      'statusCode': 418,
      'body': json.dumps('Missing request body')
    }

  return None


def is_allowed_origin(event):
  origin = event['headers']['origin'] if 'origin' in event['headers'] else None

  if origin in allowed_origins: return True

  return False

def is_options_request(event):
  return event['requestContext']['http']['method'] == 'OPTIONS'

def send_email(account, to_email, subject, content):
  # Create a secure SSL context
  context = ssl.create_default_context()

  with smtplib.SMTP_SSL(account['Server'], account['Port'], context=context) as server:
    server.login(account['User'], account['Password'])
    # Send email here
    message = "Subject: " + subject
    message = message + "\n\n\n"
    message = message + content

    server.sendmail(account['user'], to_email, message)
