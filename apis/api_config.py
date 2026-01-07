import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config import (
    PROJECT_UUID,
    WORKSPACE_ID,
    USERNAME,
    AUTH_TOKEN_KEY,
    BASE_URL,
    REQUEST_TIMEOUT,
    ENFORCE_COUNT_LIMIT,
    SEARCH_REQUEST_BODY,
)


SEARCH_API_URL = f"{BASE_URL.rstrip('/')}/api/v1/search/"
