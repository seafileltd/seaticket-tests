PROJECT_UUID = ''
WORKSPACE_ID = ''
USERNAME = ''
AUTH_TOKEN_KEY = ''

# Base URL for real integration tests (requires a running server).
BASE_URL = 'http://127.0.0.1:8000'
REQUEST_TIMEOUT = 30

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
    'connection_ids': '',
    'extra_sources': ['knowledge_base', 'ticket'],
    'search_type': 'normal_search',
}
