import time

from seatable_api import Base
from config import SEATABLE_API_TOKEN, SEATABLE_SERVER_URL, SEATABLE_TABLE_NAME


def write_simple_result(row_data):
    base = Base(SEATABLE_API_TOKEN, SEATABLE_SERVER_URL)
    base.auth()

    '''
    row_data = {
        "Operation": "Test Write",
        "Status Code": 000,
        "Response": "text",
        "Time": "1997-01-01 00:00"
    }
    '''
    base.append_row(SEATABLE_TABLE_NAME,row_data)

def get_formatted_time():
    timestamp = time.time()
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))