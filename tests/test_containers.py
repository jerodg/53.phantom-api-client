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
from time import sleep
from typing import List, Optional
from uuid import uuid4

import pytest
from os import getenv

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ArtifactRequest, Cef, ContainerRequest, RequestFilter


def generate_artifacts(artifact_count: Optional[int] = 1) -> List[ArtifactRequest]:
    artifacts = []
    for i in range(0, artifact_count):
        uid = uuid4().hex
        cef = Cef()
        artifacts.append(ArtifactRequest(cef=cef,
                                         cef_types=None,
                                         container_id=None,
                                         data=None,
                                         description=f'Test Create Artifact {i}.',
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
                                         type='test'))
        sleep(.1)  # This is necessary to ensure random uuid is unique (not always thread safe)

    return artifacts


def generate_containers(container_count: Optional[int] = 1, artifact_count: Optional[int] = 0) -> List[ContainerRequest]:
    containers = []
    for i in range(0, container_count):
        uid = uuid4().hex
        containers.append(ContainerRequest(asset_id=None,
                                           close_time=None,
                                           container_type='default',
                                           custom_fields=None,
                                           data=None,
                                           description=f'Test create container {i}.',
                                           due_time=None,
                                           end_time=None,
                                           ingest_app_id=None,
                                           kill_chain=None,
                                           label='test',
                                           name=f'Test: {uid}',
                                           owner_id=9,
                                           run_automation=False,
                                           sensitivity='green',
                                           severity='low',
                                           source_data_identifier=uid,
                                           start_time=None,
                                           open_time=None,
                                           status=None,
                                           tags=['test'],
                                           tenant_id=2,
                                           artifacts=generate_artifacts(artifact_count=artifact_count),
                                           request_id=uuid4().hex))
        sleep(.1)  # This is necessary to ensure random uuid is unique (not always thread safe)

    return containers


@pytest.mark.asyncio
async def test_get_container_count():
    ts = time.perf_counter()

    bprint('Test: Get Container Count')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        results = await pac.get_container_count()
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


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
async def test_get_containers_filtered():
    ts = time.perf_counter()

    bprint('Test: Get Containers Filtered')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        f = {'_filter_name__icontains': '"test"', '_filter_tenant': 2}
        results = await pac.get_containers(filter=RequestFilter(filter=f))

        ids = len(list(set([k['id'] for k in results.success])))
        print(f'Results: {len(results.success)} == Ids: {ids}?')

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure
        assert len(results.success) == ids  # Ensure no duplicates

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_container():
    ts = time.perf_counter()

    bprint('Test: Create Container')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_containers()
        response_results, request_results = await pac.create_containers(containers=container)

        # todo: add auto-check for container creation
        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 1
        assert not response_results.failure

        tprint(response_results, request_results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_duplicate_container():
    ts = time.perf_counter()

    bprint('Test: Create Duplicate Container')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_containers()
        response_results, request_results = await pac.create_containers(containers=container)

        # todo: add auto-check for container creation
        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 1
        assert not response_results.failure

        tprint(response_results, request_results, top=5)
        print('Creating duplicate container...')

        response_results, request_results = await pac.create_containers(containers=container)
        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 0
        assert len(response_results.failure) == 1

        tprint(response_results, request_results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_duplicate_container_update_if_exists():
    ts = time.perf_counter()

    bprint('Test: Create Duplicate Container; Update if Exists')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container = generate_containers()
        response_results, request_results = await pac.create_containers(containers=container)

        # todo: add auto-check for container creation
        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 1
        assert not response_results.failure

        tprint(response_results, request_results, top=5)
        print('Creating duplicate container...')
        container[0].description = 'Test create container; udpate if exists.'
        response_results, request_results = await pac.create_containers(containers=container)

        # todo: verify update took place
        assert type(response_results) is Results
        assert len(request_results) == 1
        assert len(response_results.success) == 0
        assert len(response_results.failure) == 1

        tprint(response_results, request_results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_containers():
    ts = time.perf_counter()

    bprint('Test: Create Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container_count = 3
        containers = generate_containers(container_count=container_count)
        response_results, request_results = await pac.create_containers(containers=containers)

        # todo: add auto-check for container creation
        assert type(response_results) is Results
        assert len(request_results) == container_count
        assert len(response_results.success) == container_count
        assert not response_results.failure

        tprint(response_results, request_results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


# @pytest.mark.asyncio
# async def test_create_container_with_customfields():
#     ts = time.perf_counter()
#
#     bprint('Test: Get Containers')
#     async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
#         uid = uuid4().hex
#         custom_fields = CustomFields(alert_source=None,
#                                      resolution_summary=None,
#                                      incident_level=None,
#                                      incident_category=None,
#                                      true_resolution=None,
#                                      analysis_completed=None,
#                                      true_detect_time=None,
#                                      analysis_started=None,
#                                      compliance_contacted=None,
#                                      contain_time=None,
#                                      vendor_ticket_number=uid,
#                                      mitigated='Not Applicable',
#                                      disposition='False Positive',
#                                      true_event_time=None,
#                                      customer_exposure='No')
#
#         tprint(results, top=5)
#
#     bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_container_with_artifact():
    ts = time.perf_counter()

    bprint('Test: Get Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container_count = 1
        artifact_count = 1
        containers = generate_containers(container_count=container_count, artifact_count=artifact_count)
        response_results, request_results = await pac.create_containers(containers=containers)

        # todo: add auto-check for container creation
        assert type(response_results) is Results
        assert len(request_results) == container_count
        assert len(response_results.success) == container_count + artifact_count
        assert not response_results.failure

        tprint(response_results, request_results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_containers_with_artifacts():
    ts = time.perf_counter()

    bprint('Test: Get Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        container_count = 1
        artifact_count = 2
        containers = generate_containers(container_count=container_count, artifact_count=artifact_count)
        containers.extend(generate_containers(container_count=container_count, artifact_count=artifact_count))

        response_results, request_results = await pac.create_containers(containers=containers)

        # todo: add auto-check for container creation
        assert type(response_results) is Results
        # assert len(request_results) == container_count
        # assert len(response_results.success) == container_count + artifact_count
        assert not response_results.failure

        tprint(response_results, request_results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')

# todo: Test create multiple containers with multiple containers (containers seem to be put into one container)
# todo: test update_existing

# @pytest.mark.asyncio
# async def test_create_container_with_comments():
#     ts = time.perf_counter()
#
#     bprint('Test: Get Containers')
#     async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
#         tprint(results, top=5)
#
#     bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
#
#
# @pytest.mark.asyncio
# async def test_create_container_with_attachments():
#     ts = time.perf_counter()
#
#     bprint('Test: Get Containers')
#     async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
#         tprint(results, top=5)
#
#     bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
