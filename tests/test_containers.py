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
from os.path import realpath

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ContainerFilter


@pytest.mark.asyncio
async def test_get_container_count():
    ts = time.perf_counter()

    bprint('Test: Get ContainerRequest Count')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_container_count()

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
        filter = ContainerFilter(page_size=100)
        # container_count = (await pac.get_container_count()).success[0]['container_count']
        # all_results = await pac.get_containers(ContainerFilter(page_size=container_count + 100))

        results = await pac.get_containers(filter)

        # difference = [i for i in results.success if i not in all_results.success]
        # print('Results difference:', difference)

        ids = len(list(set([k['id'] for k in results.success])))
        print(f'Results: {len(results.success)} == Ids: {ids}?')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert len(results.success) == ids  # Ensure no duplicates
        # If a new container is created between the get_containers calls these will not match up
        # assert container_count == len(results.success)

        print(f'Fetched {len(results.success)} containers.')
        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_containers_performance_analysis():
    ts = time.perf_counter()
    bprint('Test: Get Containers Performance Analysis')
    # Semaphore, PageSize
    semaphores = range(1, 100, 5)
    page_sizes = range(1, 100, 10)
    stats = []

    for semaphore in semaphores:
        for page_size in range(1, 100, 10):
            async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml', sem=semaphore) as pac:
                tts = time.perf_counter()
                results = await pac.get_containers(ContainerFilter(page_size=page_size))
                recs = len(results.success)
                dur = time.perf_counter() - tts
                stat = f'| {semaphore}\t| {page_size}\t| {recs}\t| {dur:f}\t| {recs / dur:f}\t|'
                stats.append(stat)
                print(stat)

    with open(realpath('./data/get_containers_stats_2019-07-30.txt')) as sfile:
        sfile.writelines(stats)

    bprint(f'-> Completed in {(time.perf_counter() - ts) / 60:f} minutes.')

# todo: test
@pytest.mark.asyncio
async def test_get_container_count_filtered():
    ts = time.perf_counter()

    bprint('Test: Get ContainerRequest Count')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_name__icontains': 'mss'}
        results = await pac.get_container_count(ContainerFilter(filter=f))

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


# todo: test
@pytest.mark.asyncio
async def test_get_containers_filtered():
    ts = time.perf_counter()

    bprint('Test: Get Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container_count = (await pac.get_container_count()).success[0]['container_count']
        # all_results = await pac.get_containers(ContainerFilter(page_size=container_count + 100))

        results = await pac.get_containers()

        # difference = [i for i in results.success if i not in all_results.success]
        # print('Results difference:', difference)

        ids = len(list(set([k['id'] for k, v in results.success.items()])))
        print(f'Results: {len(results.success)} == Ids: {ids}?')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert len(results.success) == ids  # Ensure no duplicates
        # If a new container is created between the get_containers calls these will not match up
        # assert container_count == len(results.success)

        print(f'Fetched {len(results.success)} containers.')
        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
