#!/usr/bin/env python3.8
"""Phantom API Client: Tests.Extras Update Containers Filtered
Copyright © 2019-2020 Jerod Gawne <https://github.com/jerodg/>

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
import time
from os import getenv
from typing import NoReturn

import pytest
from base_api_client import bprint, tprint
from base_api_client.models import Results

from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ContainerRequest, Query


@pytest.mark.asyncio
async def test_update_containers_filtered() -> NoReturn:
    ts = time.perf_counter()

    bprint('Test: Update Containers Filtered')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client_dev.toml') as pac:
        results = await pac.get_container_count(query=Query(type='container',
                                                            filter={'_filter_name__icontains': '"mcafee"',
                                                                    '_filter_label':           '"events"'}))
        tprint(results, top=5)

        count = results.success[0]['count']

        results = await pac.get_containers(query=Query(type='container',
                                                       filter={'_filter_name__icontains': '"mcafee"',
                                                               '_filter_label':           '"events"'}))

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

        print('Updating Containers...')

        requests = [ContainerRequest(id=i, label='mcafee') for i in [c['id'] for c in results.success]]

        results = await pac.update_records(requests=requests)

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
