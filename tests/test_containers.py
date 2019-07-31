#!/usr/bin/env python3.8
"""Phantom API Client: Test Containers
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
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ContainerFilter


@pytest.mark.asyncio
async def test_get_container_count():
    ts = time.perf_counter()

    bprint('Test: Get Container Count')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_container_count()
        print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_containers():
    ts = time.perf_counter()

    bprint('Test: Get Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_containers()

        ids = len(list(set([k['id'] for k in results.success])))
        print(f'Results: {len(results.success)} == Ids: {ids}?')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert len(results.success) == ids  # Ensure no duplicates

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_container_count_filtered():
    ts = time.perf_counter()

    bprint('Test: Get ContainerRequest Count')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_name__icontains': '"test"'}
        results = await pac.get_container_count(ContainerFilter(filter=f))

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_containers_filtered():
    ts = time.perf_counter()

    bprint('Test: Get Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_name__icontains': '"test"'}
        results = await pac.get_containers(ContainerFilter(filter=f))
        print('results:')
        print(*results, sep='\n')

        # ids = len(list(set([k['id'] for k in results.success])))
        # print(f'Results: {len(results.success)} == Ids: {ids}?')

        # assert type(results) is Results
        # assert len(results.success) >= 1
        # assert not results.failure
        # assert len(results.success) == ids  # Ensure no duplicates

        # tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
