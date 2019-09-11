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

import pytest
from os import getenv

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import Query
from tests.extras.generate_objects import generate_container


@pytest.mark.asyncio
async def test_get_all_artifacts_count():
    ts = time.perf_counter()
    bprint('Test: Get All Artifacts Count')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_artifact_count()
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)  # Should return all artifacts across all containers

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_container_artifacts_count():
    ts = time.perf_counter()
    bprint('Test: Get Container Artifacts Count')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        # todo: Get or create random test container
        results = await pac.get_artifact_count(container_id=120020)
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_artifacts():
    ts = time.perf_counter()
    bprint('Test: Get All Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_artifact_count()
        count = results.success[0]['count']

        results = await pac.get_artifacts()
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_artifact():
    ts = time.perf_counter()
    bprint('Test: Get One Artifact')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_artifacts(artifact_id=6113096)
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_container_artifacts():
    ts = time.perf_counter()
    bprint('Test: Get All Container Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        # todo: Get or create random test container
        results = await pac.get_artifact_count(container_id=120020)
        count = results.success[0]['count']
        results = await pac.get_artifacts(container_id=120020)
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_one_artifact():
    ts = time.perf_counter()
    bprint('Test: Delete One Artifact')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        # todo: Get or create random test container
        results = await pac.delete_records(ids=[6113092], query=Query(type='artifact'))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert results.success

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_artifacts():
    ts = time.perf_counter()
    bprint('Test: Delete Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        # todo: Get or create random test container
        results = await pac.delete_records(ids=[6113090, 6113089], query=Query(type='artifact'))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 2
        assert not results.failure
        assert results.success[0]['success']

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_one_artifact():
    ts = time.perf_counter()
    bprint('Test: Create One Artifact')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container(artifact_count=1)
        container[0].update_id(119109)
        response_results, request_results = await pac.create_artifacts(container)
        # print(response_results)

        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 1
        assert not response_results.failure
        assert response_results.success[0]['success']

        tprint(response_results, request_results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_artifacts():
    ts = time.perf_counter()
    bprint('Test: Create Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container(artifact_count=2)
        container[0].update_id(119109)
        response_results, request_results = await pac.create_artifacts(container)
        # print(response_results)

        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 2
        assert not response_results.failure
        assert response_results.success[0]['success']

        tprint(response_results, request_results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_update_one_artifact():
    ts = time.perf_counter()
    bprint('Test: Update One Artifact')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container(artifact_count=1)[0]
        artifact = container.artifacts[0]
        rid = artifact.data['request_id']
        artifact.clear()
        artifact.data = {'request_id': rid}
        artifact.name = 'Update Test'
        artifact.update_id(6119877)
        results = await pac.update_records(artifact)
        # print(response_results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert results.success
        assert results.success[0]['success']

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_update_artifacts():
    ts = time.perf_counter()
    bprint('Test: Update Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container(artifact_count=2)[0]
        artifacts = container.artifacts
        rids = [a.data['request_id'] for a in artifacts]
        [a.clear() for a in artifacts]
        ids = [6119877, 6119876]
        for i, a in enumerate(artifacts):
            a.data = {'request_id': rids[i]}
            a.name = f'Update Test: {i}'
            a.update_id(ids[i])

        results = await pac.update_records(artifacts)
        # print(response_results)

        assert type(results) is Results
        assert len(results.success) == 2
        assert not results.failure
        assert results.success
        assert results.success[0]['success']

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
