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
from phantom_api_client.models import ContainerQuery, Query
from tests.extras.generate_objects import generate_container


@pytest.mark.asyncio
async def test_get_containers_count():
    ts = time.perf_counter()
    bprint('Test: Get Containers Count')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_container_count()
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)  # Should return all containers across all containers

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_containers():
    ts = time.perf_counter()
    bprint('Test: Get All Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_container_count()
        count = results.success[0]['count']

        results = await pac.get_containers()
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_container():
    ts = time.perf_counter()
    bprint('Test: Get One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_containers(container_id=119109)
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_one_container():
    ts = time.perf_counter()
    bprint('Test: Create One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container()
        response_results, request_results = await pac.create_containers(container)
        # print(response_results)

        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 1
        assert not response_results.failure
        assert response_results.success[0]['success']

        tprint(response_results, request_results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_containers():
    ts = time.perf_counter()
    bprint('Test: Create Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container(container_count=2)
        response_results, request_results = await pac.create_containers(container)
        # print(response_results)

        assert type(response_results) is Results
        assert len(request_results) == 2
        assert len(response_results.success) == 2
        assert not response_results.failure
        assert response_results.success[0]['success']

        tprint(response_results, request_results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_update_one_container():
    ts = time.perf_counter()
    bprint('Test: Update One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container()[0]
        rid = container.data['request_id']
        container.clear()
        container.data = {'request_id': rid}
        container.name = 'Update Test'
        container.update_id(119109)
        results = await pac.update_records(container)
        # print(response_results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert results.success
        assert results.success[0]['success']

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_update_containers():
    ts = time.perf_counter()
    bprint('Test: Update Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        containers = generate_container(container_count=2)

        rids = [a.data['request_id'] for a in containers]
        [a.clear() for a in containers]
        ids = [119109, 119108]
        for i, a in enumerate(containers):
            a.data = {'request_id': rids[i]}
            a.name = f'Update Test: {i}'
            a.update_id(ids[i])

        results = await pac.update_records(containers)
        # print(response_results)

        assert type(results) is Results
        assert len(results.success) == 2
        assert not results.failure
        assert results.success
        assert results.success[0]['success']

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_one_container():
    ts = time.perf_counter()
    bprint('Test: Delete One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        # todo: Get or create random test container
        results = await pac.delete_records(ids=[120700], query=Query(type='container'))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert results.success

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_containers():
    ts = time.perf_counter()
    bprint('Test: Delete Containers')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        # todo: Get or create random test container
        results = await pac.delete_records(ids=[120699, 120697], query=Query(type='container'))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 2
        assert not results.failure
        assert results.success[0]['success']

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_container_whitelist_users():
    ts = time.perf_counter()
    bprint('Test: Get One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_containers(container_id=119109, query=ContainerQuery(_annotation_whitelist_users=True))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert type(results.success[0]['whitelist_users']) is list

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_container_whitelist_cadidates():
    ts = time.perf_counter()
    bprint('Test: Get One Container')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_containers(container_id=119109, query=ContainerQuery(whitelist_candidates=True))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
