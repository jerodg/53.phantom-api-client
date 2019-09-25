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
from typing import NoReturn

import pytest
from delorean import Delorean, parse
from os import getenv

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ContainerQuery


@pytest.mark.asyncio
async def test_delete_containers() -> NoReturn:
    ts = time.perf_counter()

    bprint('Test: Delete Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client_prod.toml') as pac:
        # Get test containers
        # f = {'_filter_name__icontains': '"bricata"', '_filter_tenant': 0}
        # results = await pac.get_containers(Query(type='container', filter=f))
        results = await pac.get_containers(query=ContainerQuery(type='container',
                                                                filter={'_filter_tenant':          0,
                                                                        '_filter_name__icontains': '"phishlabs"'}))
        # print('results:', len(results.success))

        # ids = [k['id'] for k in results.success]
        # print(f'Found {len(ids)} ids.')

        assert type(results) is Results
        # assert len(results.success) >= 1
        assert not results.failure

        print('Get Test Containers:')
        tprint(results, top=5)

        # Get containers older than...
        date_window = Delorean(datetime=dt.datetime(2019, 8, 1), timezone='UTC')
        date_window1 = Delorean(datetime=dt.datetime(2019, 8, 31), timezone='UTC')
        containers = []
        for result in results.success:
            st = parse(result['start_time'], dayfirst=False)

            if date_window <= st <= date_window1:
                # print('result:', result)
                # print('st:', st)
                containers.append(result)
        print(f'Found {len(containers)}, containers.')
        print(*containers, sep='\n')

        # Delete test containers
        # print('Delete Test Containers')
        # results1 = await pac.delete_records(ids=ids, query=Query(type='container'))
        #
        # assert type(results1) is Results
        # # assert len(results1.success) >= 1
        # assert not results1.failure
        #
        # tprint(results1, top=5)
        #
        # # Verify test containers have been deleted
        # results2 = await pac.get_containers(query=ContainerQuery(type='container',
        #                                                          filter={'_filter_tenant':          0,
        #                                                                  '_filter_name__icontains': '"bricata"'}))
        # print('results2', results2)
        # assert type(results2) is Results
        # assert len(results2.success) == 0
        # assert not results2.failure
        #
        # print('Get Test Containers After Delete')
        # tprint(results2, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
