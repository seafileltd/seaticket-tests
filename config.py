import os
import re
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from seatable_api import context


PROJECT_API_TOKEN = ''
SEATABLE_API_TOKEN = ''
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


def load_local_settings(module):
    '''Import any symbols that begin with A-Z. Append to lists any symbols
    that begin with "EXTRA_".
    '''
    for attr in dir(module):
        match = re.search(r'^EXTRA_(\w+)', attr)
        if match:
            name = match.group(1)
            value = getattr(module, attr)
            try:
                globals()[name] += value
            except KeyError:
                globals()[name] = value
        elif re.search(r'^[A-Z]', attr):
            globals()[attr] = getattr(module, attr)


# Load local_settings.py
try:
    import local_settings
except ImportError:
    pass
else:
    load_local_settings(local_settings)
    del local_settings