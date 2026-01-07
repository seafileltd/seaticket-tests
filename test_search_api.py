import pytest
import requests
from datetime import datetime

from config import (
    AUTH_TOKEN_KEY,
    SEARCH_REQUEST_BODY,
    BASE_URL,
    REQUEST_TIMEOUT,
    ENFORCE_COUNT_LIMIT,
)


@pytest.fixture
def base_url():
    return f"{BASE_URL.rstrip('/')}"


def get_formatted_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def post_search(base_url, _payload: dict, token: str = None, count: int = None):
    url = f"{base_url}/api/v1/search/"
    if count is not None:
        url = f"{url}?count={count}"

    payload = _payload
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


def _safe_json(resp):
    try:
        return resp.json()
    except Exception:
        return None


def _assert_json_dict(resp):
    data = _safe_json(resp)
    assert isinstance(data, dict), (
        f"Response is not JSON object. "
        f"status={resp.status_code} content_type={resp.headers.get('Content-Type')} text={resp.text}"
    )
    return data


class TestSearchViewAPI:

    def test_unauthorized_returns_403(self, base_url):
        resp = post_search(base_url, SEARCH_REQUEST_BODY)
        assert resp.status_code == 403, resp.text

    def test_missing_project_uuid_returns_400(self, base_url):
        body = dict(SEARCH_REQUEST_BODY)
        body.pop('project_uuid', None)
        resp = post_search(base_url, body, token=AUTH_TOKEN_KEY)
        assert resp.status_code == 400, resp.text

        data = _assert_json_dict(resp)
        assert 'error_msg' in data
        assert isinstance(data['error_msg'], str)

    def test_missing_workspace_id_returns_400(self, base_url):
        body = dict(SEARCH_REQUEST_BODY)
        body.pop('workspace_id', None)
        resp = post_search(base_url, body, token=AUTH_TOKEN_KEY)
        assert resp.status_code == 400, resp.text

        data = _assert_json_dict(resp)
        assert 'error_msg' in data
        assert isinstance(data['error_msg'], str)

    def test_missing_query_returns_400(self, base_url):
        body = dict(SEARCH_REQUEST_BODY)
        body.pop('query', None)
        resp = post_search(base_url, body, token=AUTH_TOKEN_KEY)
        assert resp.status_code == 400, resp.text

        data = _assert_json_dict(resp)
        assert 'error_msg' in data
        assert isinstance(data['error_msg'], str)

    def test_missing_sources_returns_400(self, base_url):
        body = dict(SEARCH_REQUEST_BODY)
        body.pop('connection_ids', None)
        body['extra_sources'] = []
        resp = post_search(base_url, body, token=AUTH_TOKEN_KEY)
        assert resp.status_code == 400, resp.text

        data = _assert_json_dict(resp)
        assert 'error_msg' in data
        assert isinstance(data['error_msg'], str)

    def test_real_search_view_integration(self, base_url):
        count = 5
        url = f"{base_url}/api/v1/search/?count={count}"
        resp = post_search(base_url, SEARCH_REQUEST_BODY, token=AUTH_TOKEN_KEY, count=count)

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
