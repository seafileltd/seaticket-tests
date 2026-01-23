import pytest
import requests

from utils import write_simple_result, get_formatted_time
from config import PROJECT_API_TOKEN, SEARCH_REQUEST_BODY, BASE_URL, REQUEST_TIMEOUT, ENFORCE_COUNT_LIMIT


@pytest.fixture
def base_url():
    return f"{BASE_URL.rstrip('/')}"


def post_search(base_url, payload: dict, token: str = None, count: int = None):
    url = f"{base_url}/api/v1/via-project-token/search/"
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
        raise AssertionError(f"request failed: {e}")

    print(f"{formatted_time} search Status Code: {response.status_code}")
    return response


def _assert_json_dict(resp):
    try:
        data =  resp.json()
    except Exception:
        data =  None
    assert isinstance(data, dict), (
        f"Response is not JSON object. "
        f"status={resp.status_code} content_type={resp.headers.get('Content-Type')} text={resp.text}"
    )
    return data


class TestSearchViewAPI:
    def test_real_search_view_integration(self, base_url):
        count = 5
        url = f"{base_url}/api/v1/search/?count={count}"
        resp = post_search(base_url, SEARCH_REQUEST_BODY, token=PROJECT_API_TOKEN, count=count)

        formatted_time = get_formatted_time()
        row_data = {
            "Operation": "Search succeeded test",
            "Status Code": resp.status_code,
            "Time": formatted_time
        }
        write_simple_result(row_data)

        assert resp.status_code == 200, (
            f"SearchView integration must return 200. "
            f"Got {resp.status_code}. "
            f"url={url}"
            f"request_body={SEARCH_REQUEST_BODY} "
            f"response_text={resp.text}"
        )

        data = _assert_json_dict(resp)

        assert 'results' in data, f"Missing 'results' in response: {data}"
        assert isinstance(data['results'], list), f"'results' is not list: {data}"
        if ENFORCE_COUNT_LIMIT:
            assert len(data['results']) <= count, f"count not enforced: count={count} len={len(data['results'])}"
