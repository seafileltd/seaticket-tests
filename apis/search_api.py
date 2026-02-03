import requests

from config import BASE_URL, REQUEST_TIMEOUT
from utils import write_simple_result, get_formatted_time


def post_search(payload: dict, token: str , count: int = None):
    search_type = payload['search_type']
    url = f"{BASE_URL.rstrip('/')}/api/v1/via-project-token/search/"
    if count is not None:
        url = f"{url}?count={count}"

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    if token:
        headers['authorization'] = f"Bearer {token}"

    formatted_time = get_formatted_time()
    response = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
    print(f"{formatted_time} post_search Status Code: {response.status_code}")

    row_data = {
        "Operation": f"{search_type}",
        "Status Code": response.status_code,
        "Time": formatted_time
    }
    write_simple_result(row_data)

    return response
