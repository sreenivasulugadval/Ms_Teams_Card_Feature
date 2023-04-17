import requests
import json

# Set up the variables for authentication
import Environment


def get_access_token():
    resource = 'https://graph.microsoft.com/'

    # Set up the Azure Active Directory OAuth2 token endpoint URL
    url = f'https://login.microsoftonline.com/{Environment.tenant_id}/oauth2/token'

    # Set up the JSON payload for the access token request
    payload = {
        'grant_type': 'client_credentials',
        'client_id': Environment.client_id,
        'client_secret': Environment.client_secret,
        'resource': resource
    }

    # Send the access token request
    response = requests.post(url, data=payload)

    # Check the response status code and parse the JSON response
    if response.status_code == 200:
        # response_json = json.loads(response.text)
        access_token = response.json()['access_token']
        print('Access token obtained successfully!')
        print("access Token : : ", response.json()['access_token'])

        # Returning Access token for requesters
        return access_token
    else:
        print('An error occurred:', response.text)
