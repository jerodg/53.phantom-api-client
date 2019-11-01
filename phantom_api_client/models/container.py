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

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Union
from uuid import uuid4

from copy import deepcopy

from base_api_client.models import Record, sort_dict
from phantom_api_client.models import ArtifactRequest
from phantom_api_client.models.custom_fields import CustomFields

logger = logging.getLogger(__name__)


@dataclass
class ContainerRequest(Record):
    asset_id: Union[int, None] = None
    close_time: Union[str, None] = None
    container_type: Union[str, None] = 'default'
    custom_fields: Union[CustomFields, dict, None] = None
    data: Union[dict, None] = field(default_factory=dict)
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
    # Below are not part of the json object but used in the helper function
    id: Union[int, List[int]] = None
    artifacts: List[ArtifactRequest] = field(default_factory=list)

    # todo: implement
    # comments: List[Comment] = field(default_factory=list)
    # attachments: List[Attachment] = field(default_factory=list)
    # audit: List[AuditRequest] = field(default_factory=list)

    def __post_init__(self):
        if self.custom_fields and type(self.custom_fields) is CustomFields:
            self.custom_fields = self.custom_fields.dict()

        try:
            self.data = {**self.data, 'request_id': uuid4().hex}
        except TypeError:
            self.data = {'request_id': uuid4().hex}

    def update_id(self, container_id: int):
        self.id = container_id

        if self.artifacts:
            for artifact in self.artifacts:
                artifact.container_id = self.id

        # todo: implement
        # if self.comments:
        #     for comment in self.comments:
        #         comment.id = self.id
        #
        # if self.attachments:
        #     for attachment in self.attachments:
        #         attachment.id = self.id

    def dict(self, cleanup: bool = True, dct: Optional[dict] = None, sort_order: str = 'asc') -> dict:
        """
        Args:
            cleanup (Optional[bool]):
            dct (Optional[dict]):
            sort_order (Optional[str]): ASC | DESC

        Returns:
            dct (dict):"""
        dct = deepcopy(self.__dict__)
        del dct['id']
        del dct['artifacts']
        # todo: implement
        # del d['comments']
        # del d['attachments']
        # del d['audit']

        if cleanup:
            dct = {k: v for k, v in dct.items() if v is not None}

        if sort_order:
            dct = sort_dict(dct, reverse=True if sort_order.lower() == 'desc' else False)

        return dct

    @property
    def end_point(self):
        return f'/container/{self.id}'


if __name__ == '__main__':
    print(__doc__)
