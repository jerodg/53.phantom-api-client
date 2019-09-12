#!/usr/bin/env python3.8
"""Phantom API Client: Test Audit
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
from random import choice

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient


@pytest.mark.asyncio
async def test_get_container_audit():
    # This needs test containers/containers created; see test_containers.py
    ts = time.perf_counter()
    bprint('Test: Get Container Audit')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_name__icontains': '"test"', '_filter_tenant': 2}
        results = await pac.get_containers(filter=ContainerRequestFilter(filter=f))
        ids = [k['id'] for k in results.success]

        results = await pac.get_audit_data(subject='container', params=choice(ids))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
