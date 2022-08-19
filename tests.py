import unittest

from serverless_mailer import the_lambda_handler as lambda_handler

class ServerlessMailerTests(unittest.TestCase):
  def test_no_origin(self):
    response = lambda_handler({
      'headers': {},
      'requestContext': { 'http': { 'method': 'GET' } }
    }, None, True)
    self.assertEqual(response['statusCode'], 403)

  def test_bad_origin(self):
    response = lambda_handler({
      'headers': { 'origin': 'https://google.com' },
      'requestContext': { 'http': { 'method': 'GET' } }
    }, None, True)
    self.assertEqual(response['statusCode'], 403)


  def test_good_origin(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'GET' } }
    }, None, True)
    self.assertNotEqual(response['statusCode'], 403)

  def test_wrong_method(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'GET' } }
    }, None, True)
    self.assertEqual(response['statusCode'], 405)

  def test_correct_post_method(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
    }, None, True)
    self.assertNotEqual(response['statusCode'], 405)

  def test_correct_options_method(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'OPTIONS' } },
    }, None, True)
    self.assertEqual(response['statusCode'], 200)
    self.assertEqual(response['headers']['Access-Control-Allow-Origin'], 'http://localhost:3000')
    self.assertEqual(response['headers']['Access-Control-Allow-Headers'], '*')
    self.assertEqual(response['headers']['Allow'], 'OPTIONS, POST')

  def test_missing_body(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
    }, None, True)
    self.assertEqual(response['statusCode'], 418)

  def test_null_body(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': None
    }, None, True)
    self.assertEqual(response['statusCode'], 418)

  def test_present_body(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': '{}'
    }, None, True)
    self.assertNotEqual(response['statusCode'], 418)

  def test_invalid_json(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': '{/%'
    }, None, True)
    self.assertEqual(response['statusCode'], 400)
    self.assertEqual(response['body'], '"Request body is not a valid JSON"')

  def test_missing_subject(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': '{"content": "hello world"}'
    }, None, True)
    self.assertEqual(response['statusCode'], 400)
    self.assertEqual(response['body'], '"Request body missing subject or content"')

  def test_missing_content(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': '{"subject": "your extended warranty"}'
    }, None, True)
    self.assertEqual(response['statusCode'], 400)
    self.assertEqual(response['body'], '"Request body missing subject or content"')

  def test_correct_content(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': '{"subject": "your extended warranty", "content": "hello world"}'
    }, None, True)
    self.assertNotEqual(response['statusCode'], 400)

  def test_bad_recipent(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': '{"to": "bill@microsoft.com", "subject": "your extended warranty","content": "hello world"}'
    }, None, True)
    self.assertEqual(response['statusCode'], 400)
    self.assertEqual(response['body'], '"The recipient is not allowed"')

  def test_good_recipent(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': '{"to": "test@email.com", "subject": "your extended warranty","content": "hello world"}'
    }, None, True)
    self.assertNotEqual(response['statusCode'], 400)

  def test_correct_send_response(self):
    response = lambda_handler({
      'headers': { 'origin': 'http://localhost:3000' },
      'requestContext': { 'http': { 'method': 'POST' } },
      'body': '{"to": "test@email.com", "subject": "your extended warranty","content": "hello world"}'
    }, None, True)
    self.assertEqual(response['statusCode'], 200)
    self.assertEqual(response['headers']['Access-Control-Allow-Origin'], 'http://localhost:3000')

if __name__ == '__main__':
  unittest.main()
