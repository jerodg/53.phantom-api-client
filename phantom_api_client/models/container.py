#!/usr/bin/env python3.8
"""Phantom API Client: Models.ContainerRequest
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
from dataclasses import dataclass, field
from typing import Any, List, Union
from uuid import uuid4

from base_api_client.models.record import Record
from phantom_api_client.models.artifact import ArtifactRequest
from phantom_api_client.models.attachment import Attachment
from phantom_api_client.models.audit import AuditRecord
from phantom_api_client.models.comment import Comment
from phantom_api_client.models.custom_fields import CustomFields


@dataclass
class ContainerRequest(Record):
    asset_id: Union[int, None] = None
    close_time: Union[str, None] = None
    container_type: Union[str, None] = 'default'
    custom_fields: Union[CustomFields, None] = None
    data: Union[dict, None] = None
    description: Union[str, None] = None
    due_time: Union[str, None] = None
    end_time: Union[str, None] = None
    ingest_app_id: Union[int, None] = None
    kill_chain: Union[str, None] = None
    label: str = None  # ContainerRequest Classification
    name: str = None  # Short Friendly ContainerRequest Name
    owner_id: Union[int, str, None] = None
    run_automation: bool = False
    sensitivity: str = 'green'
    severity: str = 'low'
    source_data_identifier: Union[str, None] = None
    start_time: Union[str, None] = None
    open_time: Union[str, None] = None
    status: Union[str, None] = 'new'
    tags: Union[str, list, None] = None
    tenant_id: Union[int, None] = None
    # Below are not part of the json object but used in the helper function
    request_id: str = uuid4().hex
    id: int = None
    artifacts: List[ArtifactRequest] = field(default_factory=list)

    # todo: implement
    # comments: List[Comment] = field(default_factory=list)
    # attachments: List[Attachment] = field(default_factory=list)
    # audit: List[AuditRequest] = field(default_factory=list)

    def __post_init__(self):
        if self.custom_fields and type(self.custom_fields) is CustomFields:
            self.custom_fields = self.custom_fields.dict()

    def update_request_id(self):
        self.request_id = uuid4().hex

    def update_id(self, id: int):
        self.id = id

        if self.artifacts:
            for artifact in self.artifacts:
                artifact.container_id = self.id

        # todo: implement
        # if self.comments:
        #     for comment in self.comments:
        #         comment.container_id = self.id
        #
        # if self.attachments:
        #     for attachment in self.attachments:
        #         attachment.container_id = self.id

    def dict(self, d: dict = None, sort_order: str = 'ASC', cleanup: bool = True) -> dict:
        """
        Args:
            d (Optional[dict]):
            sort_order (Optional[str]): ASC | DESC
            cleanup (Optional[bool]):

        Returns:
            d (dict):"""
        d = {**self.__dict__}
        # del d['request_id']
        # del d['id']
        del d['artifacts']
        # todo: implement
        # del d['comments']
        # del d['attachments']
        # del d['audit']

        if cleanup:
            d = {k: v for k, v in d.items() if v is not None}

        if sort_order:
            d = dict(sorted(d.items(), reverse=True if sort_order.lower() == 'desc' else False))

        return d


@dataclass
class ContainerRecord(Record):
    record: dict
    _pretty_artifact_update_time: Union[str, None] = None
    _pretty_asset: Union[str, None] = None
    _pretty_closing_owner: Union[str, None] = None
    _pretty_create_time: Union[str, None] = None
    _pretty_current_phase: Union[str, None] = None
    _pretty_due_time: Union[str, None] = None
    _pretty_ingest_app: Union[str, None] = None
    _pretty_owner: Union[str, None] = None
    _pretty_parent_container: Union[str, None] = None
    _pretty_past_due: Union[bool, None] = None
    _pretty_sla_delta: Union[str, None] = None
    _pretty_start_time: Union[str, None] = None
    _pretty_tenant: Union[str, None] = None
    artifact_count: Union[int, None] = None
    artifact_update_time: Union[str, dt.datetime, None] = None
    asset: Union[int, None] = None
    close_time: Union[str, dt.datetime, None] = None
    closing_owner: Union[int, None] = None
    closing_rule_run: Union[str, None] = None
    container_type: Union[str, None] = None  # Default (event) | Case
    container_update_time: Union[str, dt.datetime, None] = None
    create_time: Union[str, dt.datetime, None] = None
    current_phase: Union[str, None] = None
    custom_fields: Union[dict, None] = None
    data: Union[dict, None] = None
    description: Union[str, dt.datetime, None] = None
    due_time: Union[str, dt.datetime, None] = None
    end_time: Union[str, dt.datetime, None] = None
    hash: Union[str, None] = None
    id: Union[int, None] = None
    in_case: Union[bool, None] = None
    ingest_app: Union[str, None] = None
    kill_chain: Union[str, None] = None
    label: Union[str, None] = None
    name: Union[str, None] = None
    node_guid: Union[str, None] = None
    open_time: Union[str, dt.datetime, None] = None
    owner: Union[int, None] = None
    owner_name: Union[str, None] = None
    parent_container: Union[int, None] = None
    sensitivity: Union[str, None] = None
    severity: Union[str, None] = None
    source_data_identifier: Union[str, None] = None
    start_time: Union[str, dt.datetime, None] = None
    status: Union[str, None] = None
    tags: Union[List[str], None] = field(default_factory=list)
    tenant: Union[int, None] = None
    version: Union[int, None] = None
    # Extras
    request_id: str = None
    artifacts: Union[List[ArtifactRequest], Any] = field(default_factory=list)
    attachments: Union[List[Attachment], Any] = field(default_factory=list)
    audit_log: Union[List[AuditRecord], Any] = field(default_factory=list)
    comments: Union[List[Comment], Any] = field(default_factory=list)

    def __post_init__(self):
        super(ContainerRecord, self).load(**self.record)
        print('post_artifacts:', self.artifacts)

    def dict(self, d: dict = None, sort_order: str = 'ASC', cleanup: bool = True) -> dict:
        """
        Args:
            d (Optional[dict]):
            sort_order (Optional[str]): ASC | DESC
            cleanup (Optional[bool]):

        Returns:
            d (dict):"""
        d = {**self.__dict__}
        del d['request_id']
        del d['id']
        del d['artifacts']
        del d['comments']
        del d['attachments']

        # if type(d['attachments'][0]) is Attachment:
        #     d['attachments'] = [a.dict for a in self.attachments]
        #
        # if type(d['artifacts'][0]) is ArtifactRequest:
        #     d['artifacts'] = [a.dict for a in self.artifacts]

        if cleanup:
            del self.record
            d = {k: v for k, v in d.items() if v is not None}

        if sort_order:
            d = dict(sorted(d.items(), reverse=True if sort_order.lower() == 'desc' else False))

        return d
