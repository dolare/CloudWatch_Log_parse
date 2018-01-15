
import os
from urllib.parse import urljoin

import requests

SITE = os.environ['domain']
USERNAME = os.environ['username']
PASSWORD = os.environ['password']

TOKEN_URL = urljoin(SITE, "accounts/access_token")
FUNC_URL = urljoin(SITE, "programs/api/update_exchange_rate")


def lambda_handler(event, context):
    print('Acquiring token for user {} from {}'.format(USERNAME, TOKEN_URL))
    r = requests.post(TOKEN_URL, data={'username':USERNAME, 'password': PASSWORD})
    token = r.json()['token']
    if r.status_code != 200:
        raise RuntimeError("Failed to request token, because:" + r.text)
    print('Received token')

    result = requests.post(FUNC_URL, headers={'Authorization': 'JWT ' + token})

    if result.status_code != 200:
        raise RuntimeError("Failed to update exchange rate, because:" + result.text)

    print(result.text)
