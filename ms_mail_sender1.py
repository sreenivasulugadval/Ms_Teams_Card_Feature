import requests
import json
import Environment
import Ms_Access_Token


def send_mail(subject, body):

    # Set up the variables for the email
    to_address = Environment.to_address
    subject = subject
    body = body

    # Set up the JSON payload
    payload = {
        'message': {
            'toRecipients': [{'emailAddress': {'address': to_address}}],
            'subject': subject,
            'body': body
        },
        'saveToSentItems': 'true'
    }

    # Set up the Graph API endpoint and access token
    url = Environment.url
    access_token = Ms_Access_Token.get_access_token()

    # Send the email using the Graph API
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check the response status code
    if response.status_code == 202:
        print('Email sent successfully!')
        return 'Email sent successfully :) '
    else:
        print('An error occurred:', response.text)
        return "Error , Unable to send a mail"
