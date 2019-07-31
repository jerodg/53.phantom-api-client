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
from os.path import realpath

from base_api_client import bprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ContainerFilter


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
