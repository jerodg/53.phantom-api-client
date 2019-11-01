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
from random import choice

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ContainerQuery
from tests.extras.generate_objects import generate_container


@pytest.mark.asyncio
async def test_get__all_containers_count():
    ts = time.perf_counter()
    bprint('Test: Get All Containers Count')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_record_count(query=ContainerQuery())
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)  # Should return all containers

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_containers_count_filtered():
    ts = time.perf_counter()
    bprint('Test: Get All Containers Count Filtered')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_record_count(query=ContainerQuery())
        unfiltered = results.success[0]['count']

        results = await pac.get_record_count(query=ContainerQuery(filter={'_filter_tenant': 2}))
        filtered = results.success[0]['count']
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert unfiltered > filtered

        tprint(results)  # Should return all containers for tenant '2'

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_containers():
    ts = time.perf_counter()
    bprint('Test: Get All Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_record_count(query=ContainerQuery())
        count = results.success[0]['count']

        results = await pac.get_records(ContainerQuery())
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_containers_filtered():
    ts = time.perf_counter()
    bprint('Test: Get All Containers Filtered')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_record_count(query=ContainerQuery(filter={'_filter_tenant': 2}))
        count = results.success[0]['count']

        results = await pac.get_records(query=ContainerQuery(filter={'_filter_tenant': 2}))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_containers_date_filtered():
    ts = time.perf_counter()
    bprint('Test: Get All Containers Date Filtered')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_record_count(ContainerQuery(filter={'_filter_tenant': 2}))
        try:
            unfiltered = results.success[0]['count']
        except IndexError:
            unfiltered = 0

        print(f'Found {unfiltered} unfiltered containers.')

        results = await pac.get_records(query=ContainerQuery(date_filter_start='2019-10-01',
                                                             date_filter_field='create_time',
                                                             filter={'_filter_tenant': 2}))
        filtered = len(results.success)
        print(f'Found {filtered} filtered containers.')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert unfiltered > filtered

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_container():
    ts = time.perf_counter()
    bprint('Test: Get One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50, filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]

        results = await pac.get_records(query=ContainerQuery(id=choice(ids)))

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_container_whitelist_users():
    ts = time.perf_counter()
    bprint('Test: Get One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50, filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]

        results = await pac.get_records(query=ContainerQuery(id=choice(ids), _annotation_whitelist_users=True))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert type(results.success[0]['whitelist_users']) is list

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_container_whitelist_candidates():
    ts = time.perf_counter()
    bprint('Test: Get One Container Whitelist Candidates')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50, filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]

        results = await pac.get_records(query=ContainerQuery(id=choice(ids), whitelist_candidates=True))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_container_phases():
    ts = time.perf_counter()
    bprint('Test: Get One Container Phases')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50, filter={'_filter_container_type': '"case"'}))
        ids = [c['id'] for c in results.success]

        results = await pac.get_records(query=ContainerQuery(id=choice(ids), phases=True))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_many_containers():
    ts = time.perf_counter()
    bprint('Test: Get Many Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50, filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]

        cids = [choice(ids), choice(ids)]
        while cids[0] == cids[1]:
            cids[1] = choice(results.success)

        results = await pac.get_records(query=ContainerQuery(id=cids))

        assert type(results) is Results
        # assert len(results.success) == 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_one_container():
    ts = time.perf_counter()
    bprint('Test: Create One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        response_results, request_results = await pac.create_containers(generate_container())
        # print(response_results)

        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 1
        assert not response_results.failure
        assert response_results.success[0]['success']

        tprint(response_results, request_results)

        print('\nVerify Results from Phantom')
        results = await pac.get_records(query=ContainerQuery(filter={'_filter_id': response_results.success[0]['id']}))
        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_many_containers():
    ts = time.perf_counter()
    bprint('Test: Create Many Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        response_results, request_results = await pac.create_containers(generate_container(container_count=2))
        # print(response_results)

        assert type(response_results) is Results
        assert len(request_results) == 2
        assert len(response_results.success) == 2
        assert not response_results.failure
        assert response_results.success[0]['success']

        tprint(response_results, request_results)

        print('\nVerify Results from Phantom')
        ids = [r['id'] for r in response_results.success]
        results = await pac.get_records(query=ContainerQuery(filter={'_filter_id__in': str(ids)}))
        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_update_one_container():
    ts = time.perf_counter()
    bprint('Test: Update One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=20, filter={'_filter_tenant': 2}))
        old_container = choice(results.success)
        print(f'Container Prior Update\n\t-> {old_container}')

        container = generate_container()[0]
        container.clear()
        container.name = 'Update Test'
        container.update_id(old_container['id'])
        results = await pac.update_records(container)
        # print(response_results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert results.success
        assert results.success[0]['success']

        tprint(results)

        results = await pac.get_records(query=ContainerQuery(id=old_container['id']))
        print(f'Container After Update\n\t-> {results.success[0]}')

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_update_many_containers():
    ts = time.perf_counter()
    bprint('Test: Update Many Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50, filter={'_filter_tenant': 2}))

        old_containers = [choice(results.success), choice(results.success)]
        while old_containers[0] == old_containers[1]:
            old_containers[1] = choice(results.success)

        ocp = '\n\t-> '.join([str(d) for d in old_containers])
        print(f'Containers Prior Update\n\t-> {ocp}')

        containers = generate_container(container_count=2)

        [a.clear() for a in containers]
        for i, a in enumerate(containers):
            a.name = f'Update Test: {i}'
            a.update_id(old_containers[i]['id'])

        results = await pac.update_records(containers)

        assert type(results) is Results
        assert len(results.success) == 2
        assert not results.failure
        assert results.success
        assert results.success[0]['success']

        tprint(results)

        results = await pac.get_records(query=ContainerQuery(id=[c['id'] for c in old_containers]))
        ucp = '\n\t-> '.join([str(d) for d in results.success])
        print(f'Containers After Update\n\t-> {ucp}')

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_one_container():
    ts = time.perf_counter()
    bprint('Test: Delete One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]
        assert ids  # Need containers to test
        cid = choice(ids)

        results = await pac.delete_records(query=ContainerQuery(id=cid))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert results.success

        tprint(results)

        print('\nVerify Results from Phantom')
        results = await pac.get_records(query=ContainerQuery(filter={'_filter_id': cid}))

        assert not results.success
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_many_containers():
    ts = time.perf_counter()
    bprint('Test: Delete Many Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]
        assert ids  # Need containers to test

        cids = [choice(ids), choice(ids)]
        while cids[0] == cids[1]:
            cids[1] = choice(results.success)

        results = await pac.delete_records(query=[ContainerQuery(id=cid) for cid in cids])
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 2
        assert not results.failure
        assert results.success[0]['success']

        tprint(results)

        print('\nVerify Results from Phantom')
        results = await pac.get_records(query=ContainerQuery(filter={'_filter_id__in': str(cids)}))

        assert not results.success
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
