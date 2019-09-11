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
from time import sleep
from typing import List, Optional
from uuid import uuid4

from phantom_api_client.models import ArtifactRequest, Cef, ContainerRequest


def generate_artifact(artifact_count: Optional[int] = 1) -> List[ArtifactRequest]:
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
                                         run_automation=True,
                                         severity='low',
                                         source_data_identifier=uid,
                                         start_time=None,
                                         tags=['test'],
                                         type='test'))
        sleep(.1)  # This is necessary to ensure random uuid is unique (not always thread safe)

    return artifacts


def generate_container(container_count: Optional[int] = 1, artifact_count: Optional[int] = 0) -> List[ContainerRequest]:
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
                                           run_automation=True,
                                           sensitivity='green',
                                           severity='low',
                                           source_data_identifier=uid,
                                           start_time=None,
                                           open_time=None,
                                           status=None,
                                           tags=['test'],
                                           tenant_id=2,
                                           artifacts=generate_artifact(artifact_count=artifact_count)))
        sleep(.1)  # This is necessary to ensure random uuid is unique (not always thread safe)

    return containers
