from dataclasses import asdict
import json
import time
from typing import Optional, Union, List
from urllib.parse import urljoin

import pandas as pd
import requests
from colorama import init as colorama_init
from termcolor import colored

from metlo.config import get_config
from metlo.types.query import Filter, TimeDimension
from metlo.utils import DateTimeEncoder
from metlo.load_definitions import load_defs


def query(
    metrics: Union[str, List[str]],
    filters: List[Filter] = [],
    groups: List[str] = [],
    time_dimensions: List[TimeDimension] = [],
    limit: Optional[int] = None,
    streaming = False,
) -> Optional[pd.DataFrame]:
    colorama_init()
    if not isinstance(metrics, list):
        metrics = [metrics]

    conf = get_config()
    if not conf:
        return

    query_data = {
        'metrics': metrics,
        'filters': [asdict(e) for e in filters],
        'groups': groups,
        'time_dimensions': [asdict(e) for e in time_dimensions],
        'limit': limit,
        'streaming': streaming,
    }

    if conf.definition_dir:
        request_data = {
            'query': query_data,
            'definitions': [
                asdict(e) for e in load_defs(conf.definition_dir)
            ]
        }
    else:
        request_data = query_data

    query_url = urljoin(conf.host_name, 'api/query')
    res = requests.post(
        query_url,
        data=json.dumps(request_data, cls=DateTimeEncoder),
        headers={
            'Content-type': 'application/json',
            'Authorization': f'Bearer {conf.api_key}',
        },
    )
    if not res.ok:
        print(colored(f'Query Failed: {res.status_code}', 'red'))
        try:
            query_res = res.json()
            if 'msg' in query_res:
                msg = query_res['msg']
                print(colored(msg, 'red'))
        except:
            pass
        return
    query_res = res.json()

    if not query_res['ok']:
        print(query_res)
        return

    if query_res.get('result'):
        return pd.DataFrame(query_res['result'])
    
    poll_id = query_res['id']
    poll_url = urljoin(conf.host_name, f'api/fetch/{poll_id}')
    fetch_status = 'PENDING'
    poll_res = None

    while fetch_status in {'PENDING', 'RECEIVED', 'STARTED', 'RETRY'}:
        poll_res = requests.get(
            poll_url,
            headers={ 'Authorization': f'Bearer {conf.api_key}' },
        ).json()
        fetch_status = poll_res['status']
        time.sleep(1)
    
    if fetch_status == 'FAILURE':
        print(colored('Query Failed', 'red'))

    if poll_res.get('result'):
        return pd.DataFrame(poll_res['result'])
    if poll_res.get('status') == 'SUCCESS':
        return pd.DataFrame()

    print(poll_res)
