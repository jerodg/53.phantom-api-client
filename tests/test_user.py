#!/usr/bin/env python3.8
"""Phantom API Client: Test User
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
from random import choice

import pytest
from base_api_client import bprint, tprint
from base_api_client.models import Results

from phantom_api_client.client import PhantomApiClient
from phantom_api_client.models import UserQuery


@pytest.mark.asyncio
async def test_get_user_count():
    ts = time.perf_counter()

    bprint('Test: Get User Count')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client_dev.toml') as pac:
        results = await pac.get_record_count(query=UserQuery())
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_users():
    ts = time.perf_counter()
    bprint('Test: Get All Users')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client_dev.toml') as pac:
        results = await pac.get_record_count(query=UserQuery())
        count = results.success[0]['count']

        results = await pac.get_records(query=UserQuery())
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_user():
    # This needs test containers/containers created; see test_containers.py
    ts = time.perf_counter()
    bprint('Test: Get One User')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client_dev.toml') as pac:
        results = await pac.get_records(query=UserQuery())
        uids = [u['id'] for u in results.success]
        uid = choice(uids)
        # print(results)

        results = await pac.get_records(query=UserQuery(id=uid))

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
