import requests
from datetime import datetime

from apis.api_config import SEARCH_API_URL, AUTH_TOKEN_KEY, REQUEST_TIMEOUT


def get_formatted_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def post_search(payload: dict, token: str = AUTH_TOKEN_KEY, count: int = None):
    url = SEARCH_API_URL
    if count is not None:
        url = f"{url}?count={count}"

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    if token:
        headers['authorization'] = f"Bearer {token}"

    formatted_time = get_formatted_time()
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
    except Exception as e:
        print(f"request failed: {e}")
        raise

    print(f"{formatted_time} post_search Status Code: {response.status_code}")
    return response
