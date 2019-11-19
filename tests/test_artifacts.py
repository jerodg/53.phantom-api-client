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
from random import choice

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ArtifactQuery, ContainerQuery
from tests.extras.generate_objects import generate_container


@pytest.mark.asyncio
async def test_get_all_artifacts_count():
    ts = time.perf_counter()
    bprint('Test: Get All Artifacts Count')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_record_count(ArtifactQuery())
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)  # Should return all artifacts across all containers

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_artifacts_count_filtered():
    ts = time.perf_counter()
    bprint('Test: Get All Artifacts Count Filtered')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_record_count(ArtifactQuery())
        unfiltered = results.success[0]['count']

        results = await pac.get_record_count(ArtifactQuery(filter={'_filter_type': '"test"'}))
        filtered = results.success[0]['count']
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert unfiltered > filtered

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_container_artifacts_count():
    ts = time.perf_counter()
    bprint('Test: Get One Container Artifacts Count')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50))
        ids = [c['id'] for c in results.success if c['artifact_count'] > 1]
        cid = choice(ids)
        print(f'Container: {cid}')

        results = await pac.get_record_count(ArtifactQuery(container_id=cid))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_one_artifact():
    ts = time.perf_counter()
    bprint('Test: Get One Artifact')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ArtifactQuery(page=0, page_size=50, filter={'_filter_type': '"test"'}))
        ids = [c['id'] for c in results.success]
        aid = choice(ids)
        print(f'Artifact: {aid}')

        results = await pac.get_records(ArtifactQuery(id=6143278))

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


# fixme: This usually fails (time-out); phantoms fault
# @pytest.mark.asyncio
# async def test_get_all_artifacts():
#     ts = time.perf_counter()
#     bprint('Test: Get All Artifacts')
#
#     async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
#         results = await pac.get_record_count(ArtifactQuery())
#         count = results.success[0]['count']
#         assert count
#
#         results = await pac.get_records(ArtifactQuery())
#         # print(results)
#
#         assert type(results) is Results
#         assert len(results.success) == count
#         assert not results.failure
#
#         tprint(results, top=5)
#
#     bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_artifacts_filtered():
    ts = time.perf_counter()
    bprint('Test: Get All Artifacts Filtered')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_type': '"test"'}
        results = await pac.get_record_count(ArtifactQuery(filter=f))
        count = results.success[0]['count']
        assert count

        results = await pac.get_records(ArtifactQuery(filter=f))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_artifacts_date_filtered():
    ts = time.perf_counter()
    bprint('Test: Get All Artifacts Date Filtered')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_type': '"test"'}
        results = await pac.get_record_count(ArtifactQuery(filter=f))
        unfiltered = results.success[0]['count']
        assert unfiltered

        print(f'Found {unfiltered} unfiltered containers.')

        results = await pac.get_records(ArtifactQuery(date_filter_start='2019-09-10',
                                                      date_filter_field='create_time',
                                                      filter=f))
        filtered = len(results.success)
        print(f'Found {filtered} filtered containers.')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert unfiltered > filtered

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_container_artifacts():
    ts = time.perf_counter()
    bprint('Test: Get All Container Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50))
        ids = [c['id'] for c in results.success if c['artifact_count'] > 1]
        cid = choice(ids)

        results = await pac.get_record_count(ArtifactQuery(container_id=cid))
        count = results.success[0]['count']

        results = await pac.get_records(ArtifactQuery(container_id=cid))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_container_artifacts_date_filtered():
    # TODO: This is hard to test since we don't know what artifacts we'll encounter.

    ts = time.perf_counter()
    bprint('Test: Get All Container Artifacts Date Filtered')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_type': '"test"'}
        results = await pac.get_record_count(ArtifactQuery(filter=f))
        unfiltered = results.success[0]['count']
        assert unfiltered

        print(f'Found {unfiltered} unfiltered containers.')

        results = await pac.get_records(ArtifactQuery(date_filter_start='2019-09-10',
                                                      date_filter_field='create_time',
                                                      filter=f))
        filtered = len(results.success)
        print(f'Found {filtered} filtered containers.')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert unfiltered > filtered

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_one_artifact():
    ts = time.perf_counter()
    bprint('Test: Create One Artifact')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container(artifact_count=1)
        results = await pac.get_records(ContainerQuery(filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]
        cid = choice(ids)

        print(f'Container: {cid}')

        container[0].update_id(cid)
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
async def test_create_many_artifacts():
    ts = time.perf_counter()
    bprint('Test: Create Many Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container(artifact_count=2)
        results = await pac.get_records(ContainerQuery(filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]
        cid = choice(ids)

        print(f'Container: {cid}')

        container[0].update_id(cid)
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
async def test_create_many_artifacts():
    ts = time.perf_counter()
    bprint('Test: Create Many Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client_prod.toml') as pac:
        container = generate_container(artifact_count=2)
        results = await pac.get_records(ContainerQuery(filter={'_filter_tenant': 2}))
        ids = [c['id'] for c in results.success]
        cid = choice(ids)

        print(f'Container: {cid}')

        container[0].update_id(cid)
        response_results, request_results = await pac.create_artifacts(container)
        # print(response_results)

        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 2
        assert not response_results.failure
        assert response_results.success[0]['success']

        tprint(response_results, request_results, top=5)

        # todo: check for creation within phantom

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

        results = await pac.get_records(ArtifactQuery(filter={'_filter_type': '"test"'}))
        ids = [c['id'] for c in results.success]
        aid = choice(ids)
        artifact.update_id(aid)

        print(f'Artifact: {aid}\n\t->{artifact}')

        results = await pac.update_records(requests=[artifact])
        # print(response_results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert results.success
        assert results.success[0]['success']

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_update_many_artifacts():
    ts = time.perf_counter()
    bprint('Test: Update Many Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_container(artifact_count=2)[0]
        artifacts = container.artifacts
        rids = [a.data['request_id'] for a in artifacts]
        [a.clear() for a in artifacts]

        results = await pac.get_records(ArtifactQuery(filter={'_filter_type': '"test"'}))
        ids = [c['id'] for c in results.success]
        aids = [choice(ids), choice(ids)]

        while aids[0] == aids[1]:
            aids[1] = choice(ids)

        print(f'Artifacts: {aids}')

        for i, a in enumerate(artifacts):
            a.data = {'request_id': rids[i]}
            a.name = f'Update Test: {i}'
            a.update_id(aids[i])

        results = await pac.update_records(artifacts)
        # print(response_results)

        assert type(results) is Results
        assert len(results.success) == 2
        assert not results.failure
        assert results.success
        assert results.success[0]['success']

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_one_artifact():
    ts = time.perf_counter()
    bprint('Test: Delete One Artifact')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(ArtifactQuery(filter={'_filter_type': '"test"'}))
        ids = [c['id'] for c in results.success]
        aid = choice(ids)

        results = await pac.delete_records(query=[ArtifactQuery(id=aid)])
        # print(results)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure
        assert results.success

        tprint(results)

        print('\nVerify Results from Phantom')
        results = await pac.get_records(query=ArtifactQuery(filter={'_filter_id': aid}))

        assert not results.success
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_many_artifacts():
    ts = time.perf_counter()
    bprint('Test: Delete Many Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(ArtifactQuery(filter={'_filter_type': '"test"'}))
        ids = [c['id'] for c in results.success]
        aids = [choice(ids), choice(ids)]
        # print(results)

        while aids[0] == aids[1]:
            aids[1] = choice(ids)

        results = await pac.delete_records(query=[ArtifactQuery(id=aid) for aid in aids])

        assert type(results) is Results
        assert len(results.success) == 2
        assert not results.failure
        assert results.success[0]['success']

        tprint(results)

        print('\nVerify Results from Phantom')
        results = await pac.get_records(query=ArtifactQuery(filter={'_filter_id__in': str(aids)}))

        assert not results.success
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_all_container_artifacts():
    ts = time.perf_counter()
    bprint('Test: Delete All Container Artifacts')

    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_records(query=ContainerQuery(page=0, page_size=50))
        ids = [c['id'] for c in results.success if c['artifact_count'] > 1]
        cid = choice(ids)

        print(f'Container: {cid}')

        results = await pac.get_record_count(ArtifactQuery(container_id=cid))
        count = results.success[0]['count']

        results = await pac.get_records(ArtifactQuery(container_id=cid))
        # print(results)

        assert type(results) is Results
        assert len(results.success) == count
        assert not results.failure

        tprint(results, top=5)

        aids = [a['id'] for a in results.success]

        results = await pac.delete_records(query=[ArtifactQuery(id=aid) for aid in aids])

        tprint(results, top=5)

        print('\nVerify Results from Phantom')
        results = await pac.get_records(query=ArtifactQuery(filter={'_filter_id__in': str(aids)}))

        assert not results.success
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
