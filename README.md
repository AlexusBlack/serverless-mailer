# Serverless SMTP Mailer

Simple script for AWS lambda that allows to turn POST HTTP request into an email. Can be used to send emails from your JS code. For example you can collect all form data on static website with JS and send it to your email via serverless endpoint.

## Installation

- Create AWS lambda function with URL, no authorisation and no CORS check
- Upload copy code of `serverless_mailer.py` file into your `lambda_function.py`
- Rename `settings.example.ini` to `settings.ini` and customise with your SMTP and destination settings
- Upload to AWS into same folder as `lambda_function.py`
- Deploy, Enjoy

## Usage

- Send POST request to the AWS Lambda URL
- Body must be in JSON format and `Content-Type` should be `application/json`
- Body must contain `subject` and `content` fields
- Body can contain `to` field with email from allowed emails list
- Make sure that you send requests from one of allowed origins
