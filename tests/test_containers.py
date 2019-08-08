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
from uuid import uuid4

import pytest
from os import getenv

from base_api_client import bprint, Results, tprint
from phantom_api_client import PhantomApiClient
from phantom_api_client.models import ArtifactRequest, Cef, ContainerFilter, ContainerRequest


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
        uid = uuid4().hex
        container = ContainerRequest(asset_id=None,
                                     close_time=None,
                                     container_type='default',
                                     custom_fields=None,
                                     data=None,
                                     description='Test create container.',
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
                                     tenant_id=2)

        results = await pac.create_containers(containers=[container])

        # todo: add auto-check for container creation
        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_create_containers():
    ts = time.perf_counter()

    bprint('Test: Create Containers')
    async with PhantomApiClient(cfg=f'{getenv("CFG_HOME")}/phantom_api_client.toml') as pac:
        uid = uuid4().hex
        uid1 = uuid4().hex

        containers = [ContainerRequest(asset_id=None,
                                       close_time=None,
                                       container_type='default',
                                       custom_fields=None,
                                       data=None,
                                       description='Test create container.',
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
                                       tenant_id=2),

                      ContainerRequest(asset_id=None,
                                       close_time=None,
                                       container_type='default',
                                       custom_fields=None,
                                       data=None,
                                       description='Test create container 1.',
                                       due_time=None,
                                       end_time=None,
                                       ingest_app_id=None,
                                       kill_chain=None,
                                       label='test',
                                       name=f'Test 1: {uid}',
                                       owner_id=9,
                                       run_automation=False,
                                       sensitivity='green',
                                       severity='low',
                                       source_data_identifier=uid1,
                                       start_time=None,
                                       open_time=None,
                                       status=None,
                                       tags=['test'],
                                       tenant_id=2)]

        results = await pac.create_containers(containers=containers)

        # todo: add auto-check for container creation
        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

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
        cef = Cef()

        uid = uuid4().hex
        artifacts = [ArtifactRequest(cef=cef,
                                     cef_types=None,
                                     container_id=None,
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

        uid = uuid4().hex
        container = ContainerRequest(asset_id=None,
                                     close_time=None,
                                     container_type='default',
                                     custom_fields=None,
                                     data=None,
                                     description='Test create container w/ artifact.',
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
                                     artifacts=artifacts)
        print('container:', container)

        results = await pac.create_containers(containers=container)

        # todo: add auto-check for container creation
        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')

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
