"""Main script to execute SearchView integration operations"""

import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from apis.api_config import (
    PROJECT_UUID,
    WORKSPACE_ID,
    USERNAME,
    SEARCH_REQUEST_BODY,
    ENFORCE_COUNT_LIMIT,
)

from apis.search_api import post_search


class SearchAPITest:

    def __init__(self):
        self.count = 5

    def run_unauthorized_test(self):
        try:
            response = post_search(SEARCH_REQUEST_BODY, token=None)
        except Exception as e:
            print(f"Error in run_unauthorized_test: {e}")
            return

        print(f"unauthorized response body: {response.text}")
        assert response.status_code == 403

    def run_required_fields_tests(self):
        url_payloads = []

        payload = dict(SEARCH_REQUEST_BODY)
        payload.pop('project_uuid', None)
        url_payloads.append(('missing_project_uuid', payload))

        payload = dict(SEARCH_REQUEST_BODY)
        payload.pop('workspace_id', None)
        url_payloads.append(('missing_workspace_id', payload))

        payload = dict(SEARCH_REQUEST_BODY)
        payload.pop('query', None)
        url_payloads.append(('missing_query', payload))

        payload = dict(SEARCH_REQUEST_BODY)
        payload.pop('connection_ids', None)
        payload['extra_sources'] = []
        url_payloads.append(('missing_sources', payload))

        for name, p in url_payloads:
            try:
                response = post_search(p)
            except Exception as e:
                print(f"Error in run_required_fields_tests {name}: {e}")
                continue

            print(f"{name} response body: {response.text}")
            assert response.status_code == 400

            try:
                response_json = json.loads(response.text)
                assert isinstance(response_json.get('error_msg'), str)
            except Exception as e:
                raise AssertionError(f"{name} response not valid error json: {e} text={response.text}")

    def run_search_success_test(self):
        try:
            response = post_search(SEARCH_REQUEST_BODY, count=self.count)
        except Exception as e:
            print(f"Error in run_search_success_test: {e}")
            return

        print(f"search response body: {response.text}")
        assert response.status_code == 200

        try:
            response_json = json.loads(response.text)
        except Exception as e:
            raise AssertionError(f"response json decode error: {e} text={response.text}")

        results = response_json.get('results')
        assert isinstance(results, list), f"'results' must be list, got: {results}"

        if ENFORCE_COUNT_LIMIT:
            assert len(results) <= self.count

    def run_print_config(self):
        print("\n========== Search integration config ==========")
        print(f"project_uuid={PROJECT_UUID}")
        print(f"workspace_id={WORKSPACE_ID}")
        print(f"username={USERNAME}")


def main():
    search_test = SearchAPITest()
    search_test.run_print_config()
    search_test.run_unauthorized_test()
    search_test.run_required_fields_tests()
    search_test.run_search_success_test()

    print("\n========== All tests completed ==========")


if __name__ == "__main__":
    main()
