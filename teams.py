import json
import requests

# this function is used to send the request to teams using webhook url

def send_request_to_teams(webhook_url, Acknowledge, purpose, servername):

    try:
        request_result = Acknowledge
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": "Approval Request",
            "themeColor": "0072C6",
            "sections": [
                {
                    "activityTitle": f"Please approve this request to {purpose} the {servername}",
                    "activitySubtitle": "Request ID: 1234",
                    "activityImage": "https://www.example.com/images/request.png",
                    "facts": [
                        {
                            "name": "Requested by",
                            "value": "sreenivasulu"
                        },
                        {
                            "name": "Request details",
                            "value": f"Requesting for {purpose}"
                        },
                        {
                            "name": request_result,
                            "value": "Raghavendra B"
                        }
                    ],

                    "potentialAction": [
                        {
                            "@type": "OpenUri",
                            "name": "Approve",
                            "targets": [
                                {
                                    "os": "default",
                                    "uri": f"http://127.0.0.1:5000/approve?servername={servername}&status={purpose}"
                                }
                            ],
                        },

                        {
                            "@type": "OpenUri",
                            "name": "Reject",
                            "targets": [
                                {
                                    "os": "default",
                                    "uri": f"http://127.0.0.1:5000/reject?servername={servername}&status={purpose}"
                                }

                            ]
                        }
                    ]
                }
            ]
        }

        headers = {"Content-Type": "application/json"}

        print("message : ", message)
        response = requests.post(webhook_url, data=json.dumps(message), headers=headers)

        # potential_actions = response.json().get("potentialAction")
        response.raise_for_status()  # raises an error if the response is not 200 OK
        print("sent a message card to teams  text: ", response.text)
        return "Successfully sent an Approval Request to Teams...Please wait for approval....."

    except requests.exceptions.HTTPError as err:
        print("Error: unable to send request to teams")
        return f"Not able to send approval request to teams , Due to Below Error occurred:<br>  {err}"

    except requests.exceptions.RequestException as err:
        print("Error: unable to send request to teams")
        return f"Request Exception occurred: {err}"

    except Exception as err:
        print("Error: unable to send request to teams")
        return f"Error occurred: {err}"



def send_request_to_teams1(webhook_url, Acknowledge, purpose, servername):

    try:
        request_result = Acknowledge
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": "Approval Request",
            "themeColor": "0072C6",
            "sections": [
                {
                    "activityTitle": f"Request is {Acknowledge} to {purpose} the {servername}",
                    "activitySubtitle": "Request ID: 1234",
                    "activityImage": "https://www.example.com/images/request.png",
                    "facts": [
                        {
                            "name": "Requested by",
                            "value": "sreenivasulu"
                        },
                        {
                            "name": "Request details",
                            "value": f"Requesting for {purpose}"
                        },
                        {
                            "name": f"{request_result} by :",
                            "value": "Raghavendra B"
                        }
                    ],

                    "potentialAction": [
                        {
                            "@type": "OpenUri",
                            "name": "Approve"
                        },

                        {
                            "@type": "OpenUri",
                            "name": "Reject",

                        }
                    ]
                }
            ]
        }

        headers = {"Content-Type": "application/json"}

        print("message : ", message)
        response = requests.post(webhook_url, data=json.dumps(message), headers=headers)

        # potential_actions = response.json().get("potentialAction")
        response.raise_for_status()  # raises an error if the response is not 200 OK
        print("sent a message card to teams  text: ", response.text)
        return "Successfully sent an Approval Request to Teams...Please wait for approval....."

    except requests.exceptions.HTTPError as err:
        print("Error: unable to send request to teams")
        return f"Not able to send approval request to teams , Due to Below Error occurred:<br>  {err}"

    except requests.exceptions.RequestException as err:
        print("Error: unable to send request to teams")
        return f"Request Exception occurred: {err}"

    except Exception as err:
        print("Error: unable to send request to teams")
        return f"Error occurred: {err}"
