#!/usr/bin/env python3.8
"""Phantom API Client: Test Artifacts
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
from uuid import uuid4

import pytest
from os import getenv
from random import choice

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ArtifactRequest, Cef, RequestFilter


@pytest.mark.asyncio
async def test_get_artifact_count():
    # This needs test containers/artifacts created; see test_containers.py
    ts = time.perf_counter()

    bprint('Test: Get Artifact Count')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        # todo: get random test container with > 1 artifact or run test create
        # results = await pac.get_containers()

        results = await pac.get_artifact_count(container_id=114871)
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


# todo: test
@pytest.mark.asyncio
async def test_get_container_count_filtered():
    ts = time.perf_counter()

    bprint('Test: Get ContainerRequest Count')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_name__icontains': '"test"'}
        results = await pac.get_container_count(RequestFilter(filter=f))

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_artifacts():
    ts = time.perf_counter()

    bprint('Test: Get Artifacts')
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


# todo: test
@pytest.mark.asyncio
async def test_get_artifacts_filtered():
    ts = time.perf_counter()

    bprint('Test: Get Artifacts Filtered')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_name__icontains': '"test"', '_filter_tenant': 2}
        results = await pac.get_containers(ContainerFilter(filter=f))

        ids = len(list(set([k['id'] for k in results.success])))
        print(f'Results: {len(results.success)} == Ids: {ids}?')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert len(results.success) == ids  # Ensure no duplicates

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_artifact():
    ts = time.perf_counter()

    bprint('Test: Create Artifact')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_name__icontains': '"test"', '_filter_tenant': 2}
        results = await pac.get_containers(RequestFilter(filter=f))

        ids = list(set([k['id'] for k in results.success]))
        id = choice(ids)
        print('Adding artifact to container:', id)

        uid = uuid4().hex
        artifacts = [ArtifactRequest(cef=Cef(),
                                     cef_types=None,
                                     container_id=id,
                                     data=None,
                                     description='Test ArtifactRequest',
                                     end_time=None,
                                     ingest_app_id=None,
                                     kill_chain=None,
                                     label='artifact',
                                     name=f'Test: {uid}',
                                     owner_id=9,
                                     run_automation=False,
                                     severity='low',
                                     source_data_identifier=uid,
                                     start_time=None,
                                     tags=['test'],
                                     type='test')]
        results = await pac.create_artifacts(artifacts)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    # todo: auto-test results
    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
