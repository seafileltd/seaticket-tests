import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config import (
    PROJECT_UUID,
    WORKSPACE_ID,
    SEARCH_REQUEST_BODY,
    ENFORCE_COUNT_LIMIT,
)

from apis.search_api import post_search


class SearchAPITest:

    def __init__(self):
        self.count = 100

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


def main():
    search_test = SearchAPITest()
    search_test.run_search_success_test()

    print("\n========== All tests completed ==========")


if __name__ == "__main__":
    main()
