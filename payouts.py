from config import access_token, payoutCurrency, tokenUrl, payoutUrl, payoutEmailSubject, payoutEmailMessage, payoutNote
import requests
import time
import secrets
import string
import base64
from os import getenv
from dotenv import load_dotenv

load_dotenv()
client_id = getenv("SCLIENTID")
client_secret = getenv("SCLIENTSECRET")


def getRandomString():
    characters = string.ascii_letters + string.digits

    string_length = 12

    random_string = ''.join(secrets.choice(characters) for _ in range(string_length))
    return random_string


def getRESTAccessToken(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}".encode('utf-8')
    base64_credentials = base64.b64encode(credentials).decode('utf-8')

    token_url = tokenUrl

    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(token_url, data=data, headers=headers)
    access_token = response.json()["access_token"]
    return access_token


def userPayout(receiver, amount):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {getRESTAccessToken(client_id, client_secret)}'
    }

    batch_id = getRandomString()
    item_id = getRandomString()
    currency = payoutCurrency
    data = f'''
    {{
        "sender_batch_header": {{
            "sender_batch_id": "{batch_id}",
            "email_subject": "{payoutEmailSubject}",
            "email_message": "{payoutEmailMessage.format(amount, currency, receiver)}"
        }},
        "items": [
            {{
                "recipient_type": "EMAIL",
                "amount": {{
                    "value": "{amount}",
                    "currency": "{currency}"
                }},
                "note": "{payoutNote}",
                "sender_item_id": "{item_id}",
                "receiver": "{receiver}",
                "recipient_wallet": "PAYPAL"
            }}
        ]
    }}
    '''

    response = requests.post(payoutUrl, headers=headers, data=data)
    print(response.text)

    try:
        if "batch_header" in response.json().keys():
            return response.json()
    except KeyError:

        return None
