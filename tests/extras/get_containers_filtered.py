#!/usr/bin/env python3.8
"""Phantom API Client: Tests.Extras Containers
Copyright © 2019 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>."""
import datetime as dt
import time

import pytest
from delorean import Delorean, parse
from os import getenv

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ContainerQuery


def filter_by_date(results: Results) -> list:
    date_window = Delorean(datetime=dt.datetime(2017, 1, 1), timezone='UTC')
    date_window1 = Delorean(datetime=dt.datetime(2019, 9, 1), timezone='UTC')
    containers = []
    for result in results.success:
        st = parse(result['create_time'], dayfirst=False, timezone='UTC')

        if date_window <= st <= date_window1:
            containers.append(result)

    print(f'Found {len(containers)}, filtered containers.')
    print(*containers, sep='\n')

    return [k['artifact_id'] for k in containers]


@pytest.mark.asyncio
async def test_get_all_containers_filtered():
    ts = time.perf_counter()
    bprint('Test: Get All Containers Filtered')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client_prod.toml') as pac:
        # f = {'_filter_container_type': '"case"'}
        f = {'_filter_tenant': 0}
        # results = await pac.get_container_count(query=ContainerQuery(filter=f))
        # count = results.success[0]['count']
        # print('count:', count)

        results = await pac.get_containers(query=ContainerQuery(filter=f))
        # print(results)

        ids = list(set([r['artifact_id'] for r in results.success]))
        print('unique_ids:', len(ids))

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

        # dedup = frozenset(item.items()), item) for item in results.sucess)
        # dedup = (frozenset(item.items()),item for item in results.success)
        # dedup = dict((frozenset(item.items()), item) for item in results.success).values()
        # print('tdedsup', type(dedup))
        # print('dedup0', dedup[0])

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
