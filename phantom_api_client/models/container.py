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

from base_api_client.models.record import Record
from phantom_api_client.models.artifact import Artifact
from phantom_api_client.models.attachment import Attachment
from phantom_api_client.models.comment import Comment
from phantom_api_client.models.custom_fields import CustomFields
from phantom_api_client.models.exceptions import InvalidOptionError
from phantom_api_client.models.audit import AuditRecord


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
    run_automation: bool = True
    sensitivity: str = 'green'
    severity: str = 'low'
    source_data_identifier: Union[str, None] = None
    start_time: Union[str, None] = None
    open_time: Union[str, None] = None
    status: Union[str, None] = 'new'
    tags: Union[str, list, None] = None
    tenant_id: Union[int, None] = None

    def __post_init__(self):
        # todo: validate custom fields if status == Closed
        label_opts = ['53investigation-mailbox',
                      'crowdstrike-alerts',
                      'events',
                      'fireeye',
                      'fireeye-alerts',
                      'insiders',
                      'mss',
                      'phishlabs',
                      'qradar-offenses',
                      'securityawareness-mailbox',
                      'splunk',
                      'test',
                      'timer',
                      None]
        if self.label not in label_opts:
            raise InvalidOptionError('label', label_opts)

        kill_chain_opts = ['Reconnaissance',
                           'Weaponization',
                           'Delivery',
                           'Exploitation',
                           'Installation',
                           'Command & Control',
                           'Actions on Objectives',
                           None]
        if self.kill_chain not in kill_chain_opts:
            raise InvalidOptionError('kill_chain', kill_chain_opts)

        sensitivity_opts = ['white', 'green', 'amber', 'red', None]
        if self.sensitivity not in sensitivity_opts:
            raise InvalidOptionError('sensitivity', sensitivity_opts)

        severity_opts = ['low', 'medium', 'high', None]
        if self.severity not in severity_opts:
            raise InvalidOptionError('severity', severity_opts)

        status_opts = ['new', 'open', 'resolved', None]
        if self.status not in status_opts:
            raise InvalidOptionError('status', status_opts)

        if self.artifacts:
            if type(self.artifacts) is not list:
                self.artifacts = [self.artifacts]
            arts = []
            for a in self.artifacts:
                if type(a) is Artifact:
                    arts.append(a.dict())
                elif type(a) is dict:
                    arts.append(a)
            self.artifacts = arts
        else:
            self.artifacts = None

        if self.custom_fields and type(self.custom_fields) is CustomFields:
            self.custom_fields = self.custom_fields.dict()


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
    attachments: Union[List[Attachment], Any] = field(default_factory=list)
    comments: Union[List[Comment], Any] = field(default_factory=list)
    artifacts: Union[List[Artifact], Any] = field(default_factory=list)
    audit: Union[List[AuditRecord], Any] = field(default_factory=list)

    def __post_init__(self):
        super(ContainerRecord, self).load(self.record)

    # @property
    # def dict(self):
    #     d = self.__dict__
    #     del d['attachments']
    #     del d['artifacts']
    #
    #     return super(ContainerRequest, self).dict(d)

    # @property
    # def record(self):
    #     d = self.__dict__
    #     if type(d['attachments'][0]) is Attachment:
    #         d['attachments'] = [a.dict for a in self.attachments]
    #
    #     if type(d['artifacts'][0]) is Artifact:
    #         d['artifacts'] = [a.dict for a in self.artifacts]
    #
    #     return {k: v for k, v in d.items() if v is not None}
    #
    # def struct(self, **entries):
    #     """This will take a record and return an object."""
    #     self.__dict__.update(entries)


@dataclass
class ContainerFilter(Record):
    """
    Attributes:
        type (str): action_run|artifact|asset|app|app_run|container|playbook_run|cluster_node
        page (int): page number to retrieve
        page_size (int): how many results per page
        pretty (bool): pretty format results
        filter (dict): {'_filter_name__icontains': 'test'}
        include_expensive (bool): return all fields
        sort (str): field_name to sort on
        order (str): asc|desc

    References:
        https://my.phantom.us/4.1/docs/rest/query
    """
    page: int = None
    page_size: int = 1000
    pretty: Union[bool, int] = None
    filter: Union[dict, None] = None
    include_expensive: Union[bool, int] = None
    sort: str = None
    order: str = None
    limit: int = None

    def __post_init__(self):
        if self.include_expensive or self.pretty:
            self.page_size = 100

        if self.pretty:
            self.pretty = 1

        if self.include_expensive:
            self.include_expensive = 1

        if self.filter:
            self.load(**self.filter)
            del self.filter
