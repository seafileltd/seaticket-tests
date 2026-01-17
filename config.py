import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from seatable_api import context
from local_settings import SEATABLE_API_TOKEN, PROJECT_API_TOKEN

PROJECT_UUID = ''
WORKSPACE_ID = ''
CONNECTION_IDS = ''

# Base URL for tests (requires a running server).
BASE_URL = 'http://127.0.0.1:8000'
REQUEST_TIMEOUT = 30

SEATABLE_TABLE_NAME = 'SeaTicket tests'
SEATABLE_SERVER_URL = context.server_url or 'https://dev.seatable.cn'
# In real environments the backend may not strictly enforce the `count` query param.
# Turn this on only if the deployed search service guarantees `len(results) <= count`.
ENFORCE_COUNT_LIMIT = False

# Request body for SearchView integration test
# connection_ids example:'connection_ids': '1,2,3'
# search_type:'normal_search' or 'semantic_search'
SEARCH_REQUEST_BODY = {
    'query': 'Seafile',
    'project_uuid': PROJECT_UUID,
    'workspace_id': str(WORKSPACE_ID),
    'connection_ids': str(CONNECTION_IDS),
    'extra_sources': ['knowledge_base', 'ticket'],
    'search_type': 'normal_search',
}
