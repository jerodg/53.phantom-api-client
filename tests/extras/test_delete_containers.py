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
import time

import pytest
from os import getenv

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient, RequestFilter


# todo: write delete function 😅
@pytest.mark.asyncio
async def test_delete_containers():
    ts = time.perf_counter()

    bprint('Test: Delete Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        # Get test containers
        f = {'_filter_name__icontains': '"bricata"', '_filter_tenant': 2}
        results = await pac.get_containers(RequestFilter(filter=f))

        ids = [k['id'] for k in results.success]
        print(f'Found {len(ids)} ids.')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        print('Get Test Containers:')
        tprint(results, top=5)

        # Delete test containers
        results = await pac.delete_containers(container_ids=ids)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        print('Delete Test Containers')
        tprint(results, top=5)

        # Verify test containers have been deleted
        f = {'_filter_name__icontains': '"test"', '_filter_tenant': 2}
        results = await pac.get_containers(RequestFilter(filter=f))
        assert type(results) is Results
        assert len(results.success) == 0
        assert not results.failure

        print('Get Test Containers After Delete')
        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
