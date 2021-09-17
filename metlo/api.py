from dataclasses import asdict
import json
import time
from typing import Optional, Union, List
from urllib.parse import urljoin

import pandas as pd
import requests

from metlo.config import get_config
from metlo.types import Filter, TimeDimension
from metlo.utils import DateTimeEncoder


def query(
    metrics: Union[str, List[str]],
    filters: List[Filter] = [],
    groups: List[str] = [],
    time_dimensions: List[TimeDimension] = []
) -> Optional[pd.DataFrame]:
    if not isinstance(metrics, list):
        metrics = [metrics]

    conf = get_config()
    if not conf:
        return

    query_url = urljoin(conf.host_name, 'api/query')
    res = requests.post(
        query_url,
        data=json.dumps(
            {
                'metrics': metrics,
                'filters': [asdict(e) for e in filters],
                'groups': groups,
                'time_dimensions': [asdict(e) for e in time_dimensions],
            },
            cls=DateTimeEncoder,
        ),
        headers={
            'Content-type': 'application/json',
            'Authorization': f'Bearer {conf.api_key}',
        },
    )
    query_res = res.json()

    if not query_res['ok']:
        print(query_res)
        return
    
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
    
    if poll_res['result']:
        return pd.DataFrame(poll_res['result'])

    print(poll_res)
